#!/usr/bin/env python3
"""Collect public enterprise project documents for benchmark evaluation."""

from __future__ import annotations

import argparse
import ast
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.parse
import urllib.robotparser
import warnings
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import feedparser
from bs4 import BeautifulSoup
from markdownify import markdownify
from readability import Document


ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
PURE_DIR = CORPUS_DIR / "pure_srs"
GITHUB_PRD_DIR = CORPUS_DIR / "github_prd"
TECH_BLOG_DIR = CORPUS_DIR / "tech_blog"
MANIFEST_PATH = ROOT / "manifest.json"
SUMMARY_PATH = ROOT / "summary.json"
README_PATH = ROOT / "README.md"

PURE_HF_DATASET = "limjiayi/pure-requirements"
PURE_FALLBACK_URL = "http://nlreqdataset.isti.cnr.it/req.zip"
PURE_TARGET = 120
GITHUB_PRD_TARGET = 80
MIN_SECTION_CHARS = 500
CODE_SEARCH_MAX_ITEMS = 240
TECH_BLOG_TARGET = 15
ACADEMIC_USER_AGENT = "Mozilla/5.0 (academic research; corpus collection for thesis)"
MEITUAN_FEED_URL = "https://tech.meituan.com/feed/"
MEITUAN_ARCHIVE_URL = "https://tech.meituan.com/archive.html"
MEITUAN_ARCHIVE_FALLBACK_URL = "https://tech.meituan.com/archives"
ALIYUN_GROUPS = [
    ("PolarDB", "https://developer.aliyun.com/group/polardb/"),
    ("RocketMQ", "https://developer.aliyun.com/group/rocketmq/"),
    ("Nacos", "https://developer.aliyun.com/group/nacos/"),
    ("Higress", "https://developer.aliyun.com/group/higress/"),
    ("Aliware", "https://developer.aliyun.com/group/aliware/"),
    ("OpenSergo", "https://developer.aliyun.com/group/opensergo/"),
    ("Seata", "https://developer.aliyun.com/group/seata/"),
    ("DBKernel", "https://developer.aliyun.com/group/dbkernel/"),
]
GITHUB_API = "https://api.github.com"
GITHUB_SEARCH_QUERIES = [
    "topic:product-requirements stars:>30",
    "topic:prd stars:>30",
    "topic:requirements-engineering stars:>30",
    "topic:产品需求文档 stars:>5",
    "topic:需求文档 stars:>5",
]
GITHUB_CODE_SEARCH_QUERIES = [
    '"Product Requirements Document" filename:README.md',
    '"Product Requirements Document" path:docs extension:md',
    '"PRD" "用户故事" "验收标准" extension:md',
    '"功能需求" "非功能需求" extension:md',
    '"软件需求规格说明书" extension:md',
    '"软件工程" "需求规格" extension:md',
    '"产品需求文档" filename:README.md',
    '"产品需求文档" path:docs extension:md',
]
SKIP_REPO_TERMS = [
    "generator",
    "generate",
    "generating",
    "tool",
    "toolkit",
    "cli",
    "plugin",
    "template",
    "framework",
    "workflow",
    "skill",
    "agent",
    "claude",
    "coding assistant",
    "mcp",
    "server",
    "extension",
    "starter",
    "prompt",
    "notion",
    "atlassian",
    "demo",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subset", choices=["pure_srs", "github_prd", "tech_blog"], default="pure_srs")
    parser.add_argument("--source", choices=["meituan", "aliyun"], default="meituan")
    parser.add_argument("--target", type=int, default=PURE_TARGET)
    args = parser.parse_args()

    ensure_layout()
    if args.subset == "pure_srs":
        report = collect_pure_srs(args.target)
    elif args.subset == "github_prd":
        report = collect_github_prd(args.target)
    elif args.subset == "tech_blog":
        report = collect_tech_blog(args.source, args.target)
    else:
        raise ValueError(f"Unsupported subset: {args.subset}")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def ensure_layout() -> None:
    for directory in [
        PURE_DIR,
        GITHUB_PRD_DIR,
        TECH_BLOG_DIR,
    ]:
        directory.mkdir(parents=True, exist_ok=True)
    README_PATH.touch(exist_ok=True)


def collect_pure_srs(target: int) -> dict[str, Any]:
    reset_subset(PURE_DIR)
    manifest = [entry for entry in load_manifest() if entry.get("subset") != "pure_srs"]

    source_report: dict[str, Any] = {
        "primary_dataset": PURE_HF_DATASET,
        "primary_status": "not_attempted",
        "fallback_url": PURE_FALLBACK_URL,
        "fallback_status": "not_attempted",
        "parse_errors": [],
    }

    source_docs = load_pure_from_huggingface(source_report)
    if not source_docs:
        source_docs = load_pure_from_fallback_zip(source_report)

    entries: list[dict[str, Any]] = []
    seen_hashes: set[str] = set()
    candidate_sections: list[dict[str, str]] = []

    for doc in source_docs:
        sections = split_sections(doc["text"])
        for section_title, section_text in sections:
            candidate_sections.append(
                {
                    "title": doc["title"],
                    "source_url": doc["source_url"],
                    "source_file": doc["source_file"],
                    "section_title": section_title,
                    "section_text": section_text,
                }
            )

    for candidate in candidate_sections:
        if len(entries) >= target:
            break
        doc_id = f"pure-{len(entries) + 1:03d}"
        title = normalize_title(f"{candidate['title']} - {candidate['section_title']}")
        category = classify_requirement_section(candidate["section_title"], candidate["section_text"])
        markdown = render_markdown(
            title=title,
            source_url=candidate["source_url"],
            source_file=candidate["source_file"],
            section_title=candidate["section_title"],
            body=candidate["section_text"],
        )
        digest = sha256_text(markdown)
        if digest in seen_hashes:
            continue
        seen_hashes.add(digest)
        local_path = f"corpus/pure_srs/{doc_id}.md"
        (ROOT / local_path).write_text(markdown, encoding="utf-8")
        entries.append(
            {
                "doc_id": doc_id,
                "subset": "pure_srs",
                "title": title,
                "source_url": candidate["source_url"],
                "license": "unknown",
                "language": "en",
                "word_count": count_words(candidate["section_text"]),
                "category": category,
                "local_path": local_path,
                "sha256": digest,
            }
        )

    manifest.extend(entries)
    manifest.sort(key=lambda item: item["doc_id"])
    write_json(MANIFEST_PATH, manifest)
    write_json(SUMMARY_PATH, build_summary(manifest))

    source_report.update(
        {
            "source_documents_loaded": len(source_docs),
            "candidate_sections_over_500_chars": len(candidate_sections),
            "written_entries": len(entries),
            "skipped_after_target_cap": max(len(candidate_sections) - len(entries), 0),
        }
    )
    return source_report


def collect_github_prd(target: int) -> dict[str, Any]:
    token = load_env_value("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is missing from .env")

    reset_subset(GITHUB_PRD_DIR)
    manifest = [entry for entry in load_manifest() if entry.get("subset") != "github_prd"]
    seen_hashes = {entry.get("sha256") for entry in manifest if entry.get("sha256")}
    entries: list[dict[str, Any]] = []
    report: dict[str, Any] = {
        "target": target,
        "queries": GITHUB_SEARCH_QUERIES,
        "code_search_queries": GITHUB_CODE_SEARCH_QUERIES,
        "api_calls": 0,
        "rate_limit_hit": False,
        "skipped_repos": [],
        "content_filtered": 0,
        "repo_query_hits": {},
        "code_query_hits": {},
        "errors": [],
        "source_repos": {},
    }

    client = GitHubClient(token, report)
    preflight_code_query_hits(client, report)
    repo_candidates = search_github_repos(client, report)
    processed_repos: set[str] = set()

    for repo in repo_candidates:
        if len(entries) >= target:
            break
        full_name = repo["full_name"]
        if full_name in processed_repos:
            continue
        processed_repos.add(full_name)

        try:
            files = list_candidate_markdown_files(client, repo)
        except Exception as exc:
            report["errors"].append({"repo": full_name, "error": f"{type(exc).__name__}: {exc}"})
            continue

        for file_info in files:
            if len(entries) >= target:
                break
            try:
                content = fetch_github_file(client, repo, file_info["path"])
            except Exception as exc:
                report["errors"].append(
                    {
                        "repo": full_name,
                        "file": file_info["path"],
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
                continue

            if not (1024 <= len(content.encode("utf-8")) <= 51200):
                continue
            if not is_prd_like_content(content, file_info["path"]):
                report["content_filtered"] += 1
                continue
            original_digest = sha256_text(content)
            if original_digest in seen_hashes:
                continue
            seen_hashes.add(original_digest)

            doc_id = f"prd-{len(entries) + 1:03d}"
            title = extract_markdown_title(content) or f"{full_name} - {file_info['path']}"
            language = detect_language(content)
            license_name = repo_license_name(repo)
            markdown = render_github_markdown(
                title=title,
                repo_url=repo["html_url"],
                file_path=file_info["path"],
                license_name=license_name,
                stars=int(repo.get("stargazers_count") or 0),
                language=language,
                body=content,
            )
            digest = sha256_text(markdown)
            local_path = f"corpus/github_prd/{doc_id}.md"
            (ROOT / local_path).write_text(markdown, encoding="utf-8")
            entries.append(
                {
                    "doc_id": doc_id,
                    "subset": "github_prd",
                    "title": normalize_title(title),
                    "source_url": repo["html_url"],
                    "license": license_name,
                    "language": language,
                    "word_count": count_words(content),
                    "category": "prd",
                    "local_path": local_path,
                    "sha256": digest,
                }
            )
            source_entry = report["source_repos"].setdefault(
                full_name,
                {
                    "repo_url": repo["html_url"],
                    "stars": int(repo.get("stargazers_count") or 0),
                    "count": 0,
                },
            )
            source_entry["count"] += 1

    if len(entries) < target:
        collect_github_code_search_files(client, manifest, entries, seen_hashes, report, target)

    manifest.extend(entries)
    manifest.sort(key=lambda item: item["doc_id"])
    write_json(MANIFEST_PATH, manifest)
    write_json(SUMMARY_PATH, build_summary(manifest))
    report["written_entries"] = len(entries)
    report["by_language"] = dict(sorted(Counter(entry["language"] for entry in entries).items()))
    return report


def collect_tech_blog(source: str, target: int) -> dict[str, Any]:
    if source == "aliyun":
        return collect_aliyun_tech_blog(target)
    if source != "meituan":
        raise ValueError(f"Unsupported tech blog source: {source}")

    started = time.perf_counter()
    TECH_BLOG_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    removed_paths = [
        entry.get("local_path")
        for entry in manifest
        if entry.get("subset") == "tech_blog" and entry.get("source_site") == "美团技术团队"
    ]
    for local_path in removed_paths:
        if local_path:
            path = ROOT / local_path
            if path.exists():
                path.unlink()
    manifest = [
        entry
        for entry in manifest
        if not (entry.get("subset") == "tech_blog" and entry.get("source_site") == "美团技术团队")
    ]
    seen_hashes = {entry.get("sha256") for entry in manifest if entry.get("sha256")}

    client = PoliteWebClient(ACADEMIC_USER_AGENT, delay_seconds=1.5)
    report: dict[str, Any] = {
        "source": "美团技术团队",
        "target": target,
        "feed_url": MEITUAN_FEED_URL,
        "archive_url": MEITUAN_ARCHIVE_URL,
        "feed_candidates": 0,
        "archive_candidates": 0,
        "candidate_urls": 0,
        "written_entries": 0,
        "skipped": [],
        "errors": [],
        "http_status": {},
        "captcha_or_rate_limit": False,
    }

    robot_parser = load_robot_parser(client, "https://tech.meituan.com/robots.txt", report)
    candidates = collect_meituan_candidates(client, report)
    existing_urls: set[str] = set()
    ordered_candidates: list[dict[str, str]] = []
    for candidate in candidates:
        url = candidate["url"]
        if url in existing_urls:
            continue
        existing_urls.add(url)
        ordered_candidates.append(candidate)
    report["candidate_urls"] = len(ordered_candidates)

    entries: list[dict[str, Any]] = []
    for candidate in ordered_candidates:
        if len(entries) >= target:
            break
        url = candidate["url"]
        if robot_parser and not robot_parser.can_fetch(ACADEMIC_USER_AGENT, url):
            report["skipped"].append({"url": url, "reason": "robots disallow"})
            continue
        try:
            article = fetch_meituan_article(client, url, candidate)
        except Exception as exc:
            report["errors"].append({"url": url, "error": f"{type(exc).__name__}: {exc}"})
            continue
        status = article.get("status")
        if status:
            report["http_status"][str(status)] = report["http_status"].get(str(status), 0) + 1
        if status in {403, 429}:
            report["captcha_or_rate_limit"] = True
            report["skipped"].append({"url": url, "reason": f"HTTP {status}"})
            continue
        if article.get("captcha"):
            report["captcha_or_rate_limit"] = True
            report["skipped"].append({"url": url, "reason": "captcha/login-like page"})
            continue

        quality = evaluate_tech_blog_quality(article["content_md"])
        if not quality["accepted"]:
            report["skipped"].append({"url": url, "reason": quality["reason"]})
            continue
        digest = sha256_text(article["content_md"])
        if digest in seen_hashes:
            report["skipped"].append({"url": url, "reason": "duplicate sha256"})
            continue
        seen_hashes.add(digest)

        doc_id = next_blog_doc_id(manifest, entries)
        markdown = render_tech_blog_markdown(
            title=article["title"],
            url=url,
            source_site="美团技术团队",
            published=article.get("published") or candidate.get("published") or "unknown",
            author=article.get("author") or "unknown",
            body=article["content_md"],
        )
        local_path = f"corpus/tech_blog/{doc_id}.md"
        (ROOT / local_path).write_text(markdown, encoding="utf-8")
        entry = {
            "doc_id": doc_id,
            "subset": "tech_blog",
            "title": normalize_title(article["title"]),
            "source_url": url,
            "source_site": "美团技术团队",
            "license": "转载需注明出处 (CC-BY-like)",
            "language": "zh",
            "word_count": count_words(article["content_md"]),
            "category": "tech_blog",
            "local_path": local_path,
            "sha256": sha256_text(markdown),
        }
        entries.append(entry)

    manifest.extend(entries)
    manifest.sort(key=lambda item: item["doc_id"])
    write_json(MANIFEST_PATH, manifest)
    write_json(SUMMARY_PATH, build_summary(manifest))
    report["written_entries"] = len(entries)
    report["elapsed_seconds"] = round(time.perf_counter() - started, 2)
    report["skip_reason_top"] = Counter(item["reason"] for item in report["skipped"]).most_common(5)
    return report


class PoliteWebClient:
    def __init__(self, user_agent: str, delay_seconds: float):
        self.user_agent = user_agent
        self.delay_seconds = delay_seconds
        self.last_request_at = 0.0

    def get(self, url: str) -> requests.Response:
        elapsed = time.perf_counter() - self.last_request_at
        if self.last_request_at and elapsed < self.delay_seconds:
            time.sleep(self.delay_seconds - elapsed)
        response = requests.get(
            url,
            headers={"User-Agent": self.user_agent},
            timeout=30,
        )
        if "tech.meituan.com" in url:
            response.encoding = "utf-8"
        self.last_request_at = time.perf_counter()
        return response


def load_robot_parser(
    client: PoliteWebClient,
    robots_url: str,
    report: dict[str, Any],
) -> urllib.robotparser.RobotFileParser | None:
    try:
        response = client.get(robots_url)
        report["robots_status"] = response.status_code
        if response.status_code != 200:
            return None
        parser = urllib.robotparser.RobotFileParser()
        parser.set_url(robots_url)
        parser.parse(response.text.splitlines())
        return parser
    except Exception as exc:
        report["errors"].append({"url": robots_url, "error": f"{type(exc).__name__}: {exc}"})
        return None


def collect_meituan_candidates(client: PoliteWebClient, report: dict[str, Any]) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    try:
        response = client.get(MEITUAN_FEED_URL)
        feed = feedparser.parse(response.text)
        report["feed_candidates"] = len(feed.entries)
        for entry in feed.entries:
            link = str(entry.get("link") or "")
            if link:
                candidates.append(
                    {
                        "url": link,
                        "title": str(entry.get("title") or ""),
                        "published": str(entry.get("published") or ""),
                    }
                )
    except Exception as exc:
        report["errors"].append({"url": MEITUAN_FEED_URL, "error": f"{type(exc).__name__}: {exc}"})

    for archive_url in [MEITUAN_ARCHIVE_URL, MEITUAN_ARCHIVE_FALLBACK_URL]:
        try:
            response = client.get(archive_url)
            soup = BeautifulSoup(response.text, "html.parser")
            links: list[dict[str, str]] = []
            for anchor in soup.find_all("a", href=True):
                href = urllib.parse.urljoin(archive_url, str(anchor["href"]))
                if re.search(r"/20\d{2}/\d{2}/\d{2}/[^/]+\.html$", href):
                    links.append({"url": href, "title": anchor.get_text(" ", strip=True), "published": ""})
            if links:
                report["archive_url_used"] = archive_url
                report["archive_candidates"] = len(links)
                candidates.extend(links)
                break
            report.setdefault("archive_probe_counts", {})[archive_url] = 0
        except Exception as exc:
            report["errors"].append({"url": archive_url, "error": f"{type(exc).__name__}: {exc}"})
    return candidates


def collect_aliyun_tech_blog(target: int) -> dict[str, Any]:
    started = time.perf_counter()
    TECH_BLOG_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    removed_paths = [
        entry.get("local_path")
        for entry in manifest
        if entry.get("subset") == "tech_blog" and entry.get("source_site") == "阿里云开发者社区"
    ]
    for local_path in removed_paths:
        if local_path:
            path = ROOT / local_path
            if path.exists():
                path.unlink()
    manifest = [
        entry
        for entry in manifest
        if not (entry.get("subset") == "tech_blog" and entry.get("source_site") == "阿里云开发者社区")
    ]
    seen_hashes = {entry.get("sha256") for entry in manifest if entry.get("sha256")}

    client = PoliteWebClient(ACADEMIC_USER_AGENT, delay_seconds=1.5)
    report: dict[str, Any] = {
        "source": "阿里云开发者社区",
        "target": target,
        "groups": {},
        "written_entries": 0,
        "skipped": [],
        "errors": [],
        "http_status": {},
        "captcha_or_rate_limit": False,
    }

    robot_parser = load_robot_parser(client, "https://developer.aliyun.com/robots.txt", report)
    candidates = collect_aliyun_candidates(client, report)
    report["candidate_urls"] = len(candidates)

    entries: list[dict[str, Any]] = []
    column_counts: Counter[str] = Counter()
    for candidate in candidates:
        if len(entries) >= target or report["captcha_or_rate_limit"]:
            break
        if column_counts[candidate["column"]] >= 5:
            report["skipped"].append({"url": candidate["url"], "column": candidate["column"], "reason": "column cap reached"})
            continue
        url = candidate["url"]
        if robot_parser and not robot_parser.can_fetch(ACADEMIC_USER_AGENT, url):
            report["skipped"].append({"url": url, "column": candidate["column"], "reason": "robots disallow"})
            continue
        try:
            article = fetch_aliyun_article(client, url, candidate)
        except Exception as exc:
            report["errors"].append({"url": url, "column": candidate["column"], "error": f"{type(exc).__name__}: {exc}"})
            continue
        status = article.get("status")
        if status:
            report["http_status"][str(status)] = report["http_status"].get(str(status), 0) + 1
        if status in {403, 429}:
            report["captcha_or_rate_limit"] = True
            report["skipped"].append({"url": url, "column": candidate["column"], "reason": f"HTTP {status}"})
            break
        if article.get("captcha"):
            report["captcha_or_rate_limit"] = True
            report["skipped"].append({"url": url, "column": candidate["column"], "reason": "captcha/login-like page"})
            break
        if status != 200:
            report["skipped"].append({"url": url, "column": candidate["column"], "reason": f"HTTP {status}"})
            continue

        quality = evaluate_tech_blog_quality(article["content_md"])
        if not quality["accepted"]:
            report["skipped"].append({"url": url, "column": candidate["column"], "reason": quality["reason"]})
            continue
        digest = sha256_text(article["content_md"])
        if digest in seen_hashes:
            report["skipped"].append({"url": url, "column": candidate["column"], "reason": "duplicate sha256"})
            continue
        seen_hashes.add(digest)

        doc_id = next_blog_doc_id(manifest, entries)
        markdown = render_tech_blog_markdown(
            title=article["title"],
            url=url,
            source_site="阿里云开发者社区",
            published=article.get("published") or "unknown",
            author=article.get("author") or "unknown",
            body=article["content_md"],
            source_column=candidate["column"],
        )
        local_path = f"corpus/tech_blog/{doc_id}.md"
        (ROOT / local_path).write_text(markdown, encoding="utf-8")
        entry = {
            "doc_id": doc_id,
            "subset": "tech_blog",
            "title": normalize_title(article["title"]),
            "source_url": url,
            "source_site": "阿里云开发者社区",
            "source_column": candidate["column"],
            "license": "转载需注明出处 (CC-BY-like)",
            "language": "zh",
            "word_count": count_words(article["content_md"]),
            "category": "tech_blog",
            "local_path": local_path,
            "sha256": sha256_text(markdown),
        }
        entries.append(entry)
        column_counts[candidate["column"]] += 1

    manifest.extend(entries)
    manifest.sort(key=lambda item: item["doc_id"])
    write_json(MANIFEST_PATH, manifest)
    write_json(SUMMARY_PATH, build_summary(manifest))
    report["written_entries"] = len(entries)
    report["by_column"] = dict(sorted(column_counts.items()))
    report["elapsed_seconds"] = round(time.perf_counter() - started, 2)
    report["skip_reason_top"] = Counter(item["reason"] for item in report["skipped"]).most_common(5)
    return report


def collect_aliyun_candidates(client: PoliteWebClient, report: dict[str, Any]) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    for column, group_url in ALIYUN_GROUPS:
        group_report: dict[str, Any] = {"url": group_url, "status": None, "article_links": 0}
        report["groups"][column] = group_report
        try:
            response = client.get(group_url)
            group_report["status"] = response.status_code
            group_report["final_url"] = response.url
            group_report["content_length"] = len(response.text)
            if response.status_code in {403, 429}:
                report["captcha_or_rate_limit"] = True
                group_report["error"] = f"HTTP {response.status_code}"
                break
            if response.status_code != 200:
                continue
            if "请完成安全验证" in response.text or "captcha" in response.text.lower():
                report["captcha_or_rate_limit"] = True
                group_report["error"] = "captcha/login-like page"
                break
            soup = BeautifulSoup(response.text, "html.parser")
            links: list[dict[str, str]] = []
            for anchor in soup.find_all("a", href=True):
                href = urllib.parse.urljoin(group_url, str(anchor["href"]))
                if not re.search(r"/article/\d+", href):
                    continue
                href = href.split("?")[0].split("#")[0]
                title = anchor.get_text(" ", strip=True)
                if href in seen_urls:
                    continue
                seen_urls.add(href)
                links.append({"url": href, "title": title, "column": column})
            group_report["article_links"] = len(links)
            candidates.extend(links)
        except Exception as exc:
            group_report["error"] = f"{type(exc).__name__}: {exc}"
            report["errors"].append({"url": group_url, "column": column, "error": group_report["error"]})
    return candidates


def fetch_meituan_article(
    client: PoliteWebClient,
    url: str,
    candidate: dict[str, str],
) -> dict[str, Any]:
    response = client.get(url)
    result: dict[str, Any] = {"status": response.status_code}
    if response.status_code != 200:
        return result
    if "captcha" in response.text.lower() or "请完成安全验证" in response.text or "登录" in response.text[:1500]:
        result["captcha"] = True
        return result

    document = Document(response.text)
    content_html = document.summary()
    content_md = markdownify(content_html, heading_style="ATX").strip()
    soup = BeautifulSoup(response.text, "html.parser")
    title = document.title() or candidate.get("title") or ""
    title = re.sub(r"[-_ ]*美团技术团队.*$", "", title).strip() or candidate.get("title") or url
    author = extract_meta_content(soup, ["author", "article:author"]) or "unknown"
    published = (
        extract_meta_content(soup, ["article:published_time", "pubdate", "publishdate"])
        or candidate.get("published")
        or "unknown"
    )
    return {
        **result,
        "title": title,
        "author": author,
        "published": published,
        "content_md": content_md,
    }


def fetch_aliyun_article(
    client: PoliteWebClient,
    url: str,
    candidate: dict[str, str],
) -> dict[str, Any]:
    response = client.get(url)
    result: dict[str, Any] = {"status": response.status_code}
    if response.status_code != 200:
        return result
    if "请完成安全验证" in response.text or "captcha" in response.text.lower() or "登录" in response.text[:1500]:
        result["captcha"] = True
        return result

    soup = BeautifulSoup(response.text, "html.parser")
    title = (
        extract_meta_content(soup, ["og:title"])
        or extract_title_tag(soup)
        or candidate.get("title")
        or url
    )
    title = re.sub(r"[-_ ]*阿里云开发者社区.*$", "", title).strip()
    published = extract_meta_content(soup, ["date", "article:published_time", "pubdate", "publishdate"]) or "unknown"
    author = extract_meta_content(soup, ["author", "article:author"]) or "unknown"
    content_md = extract_aliyun_lark_markdown(response.text)
    if not content_md:
        document = Document(response.text)
        content_md = markdownify(document.summary(), heading_style="ATX").strip()
    content_md = demote_markdown_headings(content_md)
    return {
        **result,
        "title": title,
        "author": author,
        "published": published,
        "content_md": content_md,
    }


def extract_aliyun_lark_markdown(html_text: str) -> str:
    match = re.search(r"GLOBAL_CONFIG\.larkContent\s*=\s*'(.*?)';", html_text, re.DOTALL)
    if not match:
        return ""
    raw = match.group(1)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            content_html = ast.literal_eval("'" + raw + "'")
    except Exception:
        content_html = raw
    content_html = content_html.replace("\\/", "/")
    soup = BeautifulSoup(content_html, "html.parser")
    for tag in soup.find_all(["meta", "card"]):
        tag.decompose()
    for tag in soup.find_all(True):
        tag.attrs = {}
    markdown = markdownify(str(soup), heading_style="ATX").strip()
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return remove_surrogates(markdown).strip()


def extract_title_tag(soup: BeautifulSoup) -> str | None:
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return None


def demote_markdown_headings(markdown: str) -> str:
    lines: list[str] = []
    for line in markdown.splitlines():
        if line.startswith("#"):
            match = re.match(r"^(#{1,5})(\s+.*)$", line)
            if match:
                lines.append("#" + match.group(1) + match.group(2))
                continue
        lines.append(line)
    return "\n".join(lines).strip()


def remove_surrogates(text: str) -> str:
    return text.encode("utf-8", errors="ignore").decode("utf-8")


def extract_meta_content(soup: BeautifulSoup, names: list[str]) -> str | None:
    for name in names:
        tag = soup.find("meta", attrs={"name": name}) or soup.find("meta", attrs={"property": name})
        if tag and tag.get("content"):
            return str(tag["content"]).strip()
    return None


def evaluate_tech_blog_quality(markdown: str) -> dict[str, Any]:
    plain = strip_markdown(markdown)
    char_count = len(re.findall(r"[\u4e00-\u9fff]", plain))
    h2_count = len(re.findall(r"^##\s+", markdown, re.MULTILINE))
    entities = extract_chinese_technical_entities(plain)
    keyword_terms = [
        "需求",
        "需求背景",
        "技术方案",
        "系统设计",
        "架构设计",
        "模块",
        "服务",
        "接口",
        "数据库",
        "数据表",
        "流程",
        "链路",
        "处理流程",
    ]

    features = []
    if sum(1 for term in keyword_terms if term in plain) >= 3:
        features.append("keywords")
    if len(entities) >= 3:
        features.append("entities")
    if 1500 <= char_count <= 15000:
        features.append("length")
    if h2_count >= 3:
        features.append("structure")

    if len(features) >= 2:
        return {"accepted": True, "features": features, "char_count": char_count, "h2_count": h2_count}
    return {
        "accepted": False,
        "features": features,
        "reason": f"quality features <2 ({','.join(features) or 'none'}; chars={char_count}; h2={h2_count}; entities={len(entities)})",
    }


def extract_chinese_technical_entities(text: str) -> set[str]:
    entities: set[str] = set()
    suffixes = "系统|平台|服务|模块|接口|数据库|数据表|引擎|网关|链路|框架|模型|组件|集群|队列|中心|中台|客户端|服务端"
    for match in re.finditer(rf"[\u4e00-\u9fffA-Za-z0-9_-]{{2,24}}(?:{suffixes})", text):
        value = match.group(0).strip()
        if 2 <= len(value) <= 32:
            entities.add(value)
    for match in re.finditer(r"\b[A-Z][A-Za-z0-9_-]{2,}\b", text):
        entities.add(match.group(0))
    return entities


def strip_markdown(markdown: str) -> str:
    text = re.sub(r"```.*?```", " ", markdown, flags=re.DOTALL)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", text)
    text = re.sub(r"[#>*_`|~-]", " ", text)
    return re.sub(r"\s+", " ", text)


def render_tech_blog_markdown(
    *,
    title: str,
    url: str,
    source_site: str,
    published: str,
    author: str,
    body: str,
    source_column: str | None = None,
) -> str:
    column_line = f"Source column: {source_column}\n" if source_column else ""
    return (
        f"# {title}\n\n"
        f"Source: {url}\n"
        f"Source site: {source_site}\n"
        f"{column_line}"
        f"Published: {published}\n"
        f"Author: {author or 'unknown'}\n"
        f"License: 转载需注明出处 (CC-BY-like)\n"
        f"Language: zh\n\n"
        f"---\n\n"
        f"{body.strip()}\n"
    )


def next_blog_doc_id(manifest: list[dict[str, Any]], pending_entries: list[dict[str, Any]]) -> str:
    max_id = 0
    for entry in [*manifest, *pending_entries]:
        doc_id = str(entry.get("doc_id") or "")
        match = re.fullmatch(r"blog-(\d+)", doc_id)
        if match:
            max_id = max(max_id, int(match.group(1)))
    return f"blog-{max_id + 1:03d}"


def preflight_code_query_hits(client: "GitHubClient", report: dict[str, Any]) -> None:
    for query in GITHUB_CODE_SEARCH_QUERIES:
        try:
            result = client.get(f"{GITHUB_API}/search/code", params={"q": query, "per_page": 1})
        except requests.HTTPError as exc:
            report["errors"].append({"query": query, "error": f"{type(exc).__name__}: {exc}"})
            continue
        if isinstance(result, dict):
            report["code_query_hits"][query] = int(result.get("total_count") or 0)


def collect_github_code_search_files(
    client: "GitHubClient",
    manifest: list[dict[str, Any]],
    entries: list[dict[str, Any]],
    seen_hashes: set[str],
    report: dict[str, Any],
    target: int,
) -> None:
    repo_cache: dict[str, dict[str, Any]] = {}
    seen_files: set[str] = set()
    inspected_items = 0

    for query in GITHUB_CODE_SEARCH_QUERIES:
        if len(entries) >= target or inspected_items >= CODE_SEARCH_MAX_ITEMS:
            break
        for page in range(1, 2):
            if len(entries) >= target or inspected_items >= CODE_SEARCH_MAX_ITEMS:
                break
            try:
                result = client.get(
                    f"{GITHUB_API}/search/code",
                    params={"q": query, "sort": "indexed", "order": "desc", "per_page": 50, "page": page},
                )
            except requests.HTTPError as exc:
                report["errors"].append({"query": query, "error": f"{type(exc).__name__}: {exc}"})
                break

            items = result.get("items", []) if isinstance(result, dict) else []
            if page == 1 and isinstance(result, dict):
                report["code_query_hits"][query] = int(result.get("total_count") or 0)
            if not items:
                break

            for item in items:
                if len(entries) >= target or inspected_items >= CODE_SEARCH_MAX_ITEMS:
                    break
                inspected_items += 1
                repo_ref = item.get("repository") or {}
                full_name = repo_ref.get("full_name")
                file_path = str(item.get("path") or "")
                if not full_name or not is_allowed_github_path(file_path):
                    continue
                file_key = f"{full_name}:{file_path}"
                if file_key in seen_files:
                    continue
                seen_files.add(file_key)

                try:
                    repo = repo_cache.get(full_name)
                    if repo is None:
                        repo = client.get(f"{GITHUB_API}/repos/{full_name}")
                        if not isinstance(repo, dict):
                            continue
                        repo_cache[full_name] = repo
                    if int(repo.get("stargazers_count") or 0) <= min_stars_for_query(query):
                        continue
                    content_response = client.get(str(item["url"]))
                    content = decode_github_content_response(content_response)
                except Exception as exc:
                    report["errors"].append(
                        {
                            "repo": full_name,
                            "file": file_path,
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )
                    continue

                if not (1024 <= len(content.encode("utf-8")) <= 51200):
                    continue
                if not is_prd_like_content(content, file_path):
                    report["content_filtered"] += 1
                    continue
                original_digest = sha256_text(content)
                if original_digest in seen_hashes:
                    continue
                seen_hashes.add(original_digest)

                doc_id = f"prd-{len(entries) + 1:03d}"
                title = extract_markdown_title(content) or f"{full_name} - {file_path}"
                language = detect_language(content)
                license_name = repo_license_name(repo)
                markdown = render_github_markdown(
                    title=title,
                    repo_url=repo["html_url"],
                    file_path=file_path,
                    license_name=license_name,
                    stars=int(repo.get("stargazers_count") or 0),
                    language=language,
                    body=content,
                )
                digest = sha256_text(markdown)
                local_path = f"corpus/github_prd/{doc_id}.md"
                (ROOT / local_path).write_text(markdown, encoding="utf-8")
                entries.append(
                    {
                        "doc_id": doc_id,
                        "subset": "github_prd",
                        "title": normalize_title(title),
                        "source_url": repo["html_url"],
                        "license": license_name,
                        "language": language,
                        "word_count": count_words(content),
                        "category": "prd",
                        "local_path": local_path,
                        "sha256": digest,
                    }
                )
                source_entry = report["source_repos"].setdefault(
                    full_name,
                    {
                        "repo_url": repo["html_url"],
                        "stars": int(repo.get("stargazers_count") or 0),
                        "count": 0,
                    },
                )
                source_entry["count"] += 1

            if len(items) < 50:
                break
    report["code_search_items_inspected"] = inspected_items


class GitHubClient:
    def __init__(self, token: str, report: dict[str, Any]):
        self.token = token
        self.report = report

    def get(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "enterprise-project-docs-corpus-builder",
        }
        self.report["api_calls"] += 1
        response = requests.get(url, headers=headers, params=params, timeout=20)
        if response.status_code in {403, 429} and response.headers.get("X-RateLimit-Remaining") == "0":
            self.report["rate_limit_hit"] = True
        response.raise_for_status()
        return response.json()


def search_github_repos(client: GitHubClient, report: dict[str, Any]) -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    seen: set[str] = set()
    for query in GITHUB_SEARCH_QUERIES:
        for page in range(1, 4):
            result = client.get(
                f"{GITHUB_API}/search/repositories",
                params={"q": query, "sort": "stars", "order": "desc", "per_page": 50, "page": page},
            )
            if page == 1 and isinstance(result, dict):
                report["repo_query_hits"][query] = int(result.get("total_count") or 0)
            items = result.get("items", []) if isinstance(result, dict) else []
            if not items:
                break
            for repo in items:
                full_name = repo.get("full_name")
                if full_name and full_name not in seen:
                    seen.add(full_name)
                    repos.append(repo)
            if len(items) < 50:
                break
    report["repo_candidates"] = len(repos)
    return sorted(
        repos,
        key=lambda repo: (repo.get("language") != "Chinese", -(repo.get("stargazers_count") or 0)),
    )


def should_skip_repo(repo: dict[str, Any]) -> str | None:
    name = str(repo.get("name") or "").lower()
    description = str(repo.get("description") or "").lower()
    haystack = f"{name} {description}"
    for term in SKIP_REPO_TERMS:
        if term in haystack:
            return f"repo name/description contains '{term}'"
    return None


def min_stars_for_query(query: str) -> int:
    return 5 if has_cjk(query) else 30


def has_cjk(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def list_candidate_markdown_files(client: GitHubClient, repo: dict[str, Any]) -> list[dict[str, Any]]:
    full_name = repo["full_name"]
    branch = repo.get("default_branch") or "main"
    tree = client.get(f"{GITHUB_API}/repos/{full_name}/git/trees/{branch}", params={"recursive": "1"})
    items = tree.get("tree", []) if isinstance(tree, dict) else []
    candidates: list[dict[str, Any]] = []
    for item in items:
        path = str(item.get("path") or "")
        size = int(item.get("size") or 0)
        lowered = path.lower()
        if item.get("type") != "blob":
            continue
        if is_allowed_github_path(path):
            if 1024 <= size <= 51200:
                candidates.append({"path": path, "size": size})
    return sorted(candidates, key=lambda item: (item["path"].lower() != "readme.md", item["path"].lower()))


def is_allowed_github_path(path: str) -> bool:
    lowered = path.lower()
    return lowered == "readme.md" or (lowered.startswith("docs/") and lowered.endswith(".md"))


def fetch_github_file(client: GitHubClient, repo: dict[str, Any], file_path: str) -> str:
    full_name = repo["full_name"]
    branch = repo.get("default_branch") or "main"
    result = client.get(f"{GITHUB_API}/repos/{full_name}/contents/{file_path}", params={"ref": branch})
    return decode_github_content_response(result)


def decode_github_content_response(result: dict[str, Any] | list[Any]) -> str:
    if not isinstance(result, dict):
        raise ValueError("unexpected GitHub contents response")
    content = result.get("content")
    encoding = result.get("encoding")
    if encoding != "base64" or not isinstance(content, str):
        raise ValueError("GitHub contents response did not include base64 content")
    return base64.b64decode(content).decode("utf-8", errors="replace").strip()


def is_prd_like_content(content: str, file_path: str) -> bool:
    lowered = content.lower()
    path = file_path.lower()
    path_text = f"{path}\n{lowered}"
    feature_a_terms = [
        "product requirements document",
        "product requirement document",
        "prd",
        "functional requirements",
        "non-functional requirements",
        "non functional requirements",
        "user stories",
        "user story",
        "acceptance criteria",
        "business requirements",
        "software requirements specification",
        "srs",
        "产品需求文档",
        "产品需求",
        "功能需求",
        "非功能需求",
        "验收标准",
        "用户故事",
        "需求描述",
        "需求说明",
        "功能列表",
        "功能清单",
        "技术方案",
        "设计方案",
        "评审记录",
        "决策记录",
    ]
    feature_b_terms = [
        "## background",
        "## goals",
        "## scope",
        "## requirements",
        "## functional",
        "## non-functional",
        "## user stories",
        "## acceptance criteria",
        "## milestones",
        "## decisions",
        "## risks",
        "## 背景",
        "## 目标",
        "## 范围",
        "## 需求",
        "## 功能",
        "## 非功能",
        "## 用户故事",
        "## 验收",
        "## 里程碑",
        "## 风险",
    ]
    feature_c_patterns = [
        r"\bshall\b",
        r"\bmust\b",
        r"\bshould\b",
        r"\bas a user\b",
        r"\bgiven\b.+\bwhen\b.+\bthen\b",
        r"\bfr[-_ ]?\d+",
        r"\bnfr[-_ ]?\d+",
        r"\breq[-_ ]?\d+",
        r"系统应",
        r"用户可以",
        r"必须",
        r"应当",
        r"需要",
        r"支持",
    ]
    feature_d_terms = ["prd", "requirement", "requirements", "srs", "product", "产品需求", "需求规格", "需求文档"]

    features = 0
    if sum(1 for term in feature_a_terms if term in path_text) >= 2:
        features += 1
    if any(term in path_text for term in feature_b_terms):
        features += 1
    if sum(1 for pattern in feature_c_patterns if re.search(pattern, lowered, re.IGNORECASE)) >= 2:
        features += 1
    if any(term in path for term in feature_d_terms):
        features += 1
    return features >= 2


def render_github_markdown(
    *,
    title: str,
    repo_url: str,
    file_path: str,
    license_name: str,
    stars: int,
    language: str,
    body: str,
) -> str:
    return (
        f"# {title}\n\n"
        f"Source: {repo_url}\n"
        f"Source file: {file_path}\n"
        f"License: {license_name}\n"
        f"Stars: {stars}\n"
        f"Language: {language}\n\n"
        f"---\n\n"
        f"{body.strip()}\n"
    )


def extract_markdown_title(content: str) -> str | None:
    for line in content.splitlines():
        value = line.strip()
        if value.startswith("# "):
            return value[2:].strip()
    return None


def detect_language(content: str) -> str:
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", content))
    latin_words = len(re.findall(r"[A-Za-z]+", content))
    return "zh" if chinese_chars >= 50 and chinese_chars >= latin_words * 0.12 else "en"


def repo_license_name(repo: dict[str, Any]) -> str:
    license_info = repo.get("license")
    if isinstance(license_info, dict):
        return str(license_info.get("spdx_id") or license_info.get("name") or "unknown")
    return "unknown"


def load_pure_from_huggingface(report: dict[str, Any]) -> list[dict[str, str]]:
    try:
        from datasets import load_dataset

        dataset = load_dataset(PURE_HF_DATASET)
    except Exception as exc:
        report["primary_status"] = f"{type(exc).__name__}: {exc}"
        return []

    docs: list[dict[str, str]] = []
    for split_name, split in dataset.items():
        for index, row in enumerate(split):
            text = longest_text_field(row)
            if len(text) < MIN_SECTION_CHARS:
                continue
            title = str(row.get("title") or row.get("name") or row.get("id") or f"{split_name}-{index}")
            docs.append(
                {
                    "title": title,
                    "text": clean_text(text),
                    "source_url": f"https://huggingface.co/datasets/{PURE_HF_DATASET}",
                    "source_file": f"{split_name}:{index}",
                }
            )
    report["primary_status"] = f"loaded {len(docs)} documents"
    return docs


def load_pure_from_fallback_zip(report: dict[str, Any]) -> list[dict[str, str]]:
    docs: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="pure_srs_") as tmp:
        tmpdir = Path(tmp)
        zip_path = tmpdir / "req.zip"
        response = requests.get(PURE_FALLBACK_URL, timeout=120)
        response.raise_for_status()
        zip_path.write_bytes(response.content)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(tmpdir / "extract")

        req_dir = tmpdir / "extract" / "req"
        for source_path in sorted(req_dir.iterdir()):
            if not source_path.is_file():
                continue
            text, error = extract_text(source_path)
            if error:
                report["parse_errors"].append({"source_file": source_path.name, "error": error})
                continue
            text = clean_text(text)
            if len(text) < MIN_SECTION_CHARS:
                report["parse_errors"].append({"source_file": source_path.name, "error": "text shorter than 500 characters"})
                continue
            docs.append(
                {
                    "title": source_path.stem,
                    "text": text,
                    "source_url": PURE_FALLBACK_URL,
                    "source_file": source_path.name,
                }
            )
    report["fallback_status"] = f"loaded {len(docs)} documents"
    return docs


def extract_text(path: Path) -> tuple[str, str | None]:
    suffix = path.suffix.lower()
    try:
        if suffix == ".pdf":
            return run_text_command(["pdftotext", str(path), "-"])
        if suffix in {".doc", ".rtf"}:
            return run_text_command(["textutil", "-convert", "txt", "-stdout", str(path)])
        if suffix in {".html", ".htm"}:
            html_text = path.read_text(errors="ignore")
            return BeautifulSoup(html_text, "html.parser").get_text("\n"), None
    except Exception as exc:
        return "", f"{type(exc).__name__}: {exc}"
    return "", f"unsupported extension: {suffix}"


def run_text_command(command: list[str]) -> tuple[str, str | None]:
    executable = shutil.which(command[0])
    if executable is None:
        return "", f"missing command: {command[0]}"
    result = subprocess.run(command, capture_output=True, text=True, timeout=90, check=False)
    if result.returncode != 0:
        return "", result.stderr.strip() or f"{command[0]} exited {result.returncode}"
    return result.stdout, None


def split_sections(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    headings: list[tuple[int, str]] = []
    seen: set[str] = set()
    heading_re = re.compile(
        r"^(?P<num>(?:chapter\s+)?\d{1,2}(?:\.0)?)(?:[\.)])?\s+"
        r"(?P<title>[A-Z][A-Za-z0-9 /,;&:()\-]{2,120})$",
        re.IGNORECASE,
    )

    for index, line in enumerate(lines):
        value = line.strip()
        match = heading_re.match(value)
        if not match or re.search(r"\.{3,}", value):
            continue
        number = match.group("num").lower().replace("chapter", "").strip()
        if not re.fullmatch(r"\d{1,2}(?:\.0)?", number):
            continue
        title = match.group("title").strip()
        marker = f"{number}:{title.lower()}"
        if marker in seen:
            continue
        seen.add(marker)
        headings.append((index, value))

    if len(headings) < 2:
        return [("Document", text)] if len(text) > MIN_SECTION_CHARS else []

    sections: list[tuple[str, str]] = []
    for position, (start, heading) in enumerate(headings):
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        body = "\n".join(lines[start:end]).strip()
        if len(body) > MIN_SECTION_CHARS:
            sections.append((heading, body))
    return sections


def clean_text(text: str) -> str:
    text = text.replace("\ufeff", "").replace("\x0c", "\n")
    lines: list[str] = []
    for line in text.splitlines():
        value = " ".join(line.strip().split())
        if not value:
            lines.append("")
        elif re.search(r"\.{4,}\s*\d+\s*$", value):
            continue
        elif value.lower() in {"table of contents", "contents"}:
            continue
        else:
            lines.append(value)
    output = "\n".join(lines)
    output = re.sub(r"\n{3,}", "\n\n", output)
    return output.strip()


def render_markdown(
    *,
    title: str,
    source_url: str,
    source_file: str,
    section_title: str,
    body: str,
) -> str:
    return (
        f"# {title}\n\n"
        f"Source: {source_url}\n\n"
        f"Source file: {source_file}\n\n"
        f"Section: {section_title}\n\n"
        f"{body.strip()}\n"
    )


def classify_requirement_section(section_title: str, section_text: str) -> str:
    probe = f"{section_title}\n{section_text[:1200]}".lower()
    non_functional_terms = [
        "non-functional",
        "non functional",
        "performance",
        "security",
        "reliability",
        "availability",
        "usability",
        "maintainability",
        "safety",
        "quality",
    ]
    if any(term in probe for term in non_functional_terms):
        return "non_functional_req"
    return "functional_req"


def longest_text_field(row: dict[str, Any]) -> str:
    candidates = [value for value in row.values() if isinstance(value, str)]
    if not candidates:
        return ""
    return max(candidates, key=len)


def normalize_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    return title[:180]


def count_words(text: str) -> int:
    latin_words = len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text))
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    return latin_words + chinese_chars


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def reset_subset(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for child in path.glob("*.md"):
        child.unlink()


def load_manifest() -> list[dict[str, Any]]:
    if not MANIFEST_PATH.exists():
        return []
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def build_summary(manifest: list[dict[str, Any]]) -> dict[str, Any]:
    by_subset = Counter(entry["subset"] for entry in manifest)
    by_language = Counter(entry["language"] for entry in manifest)
    return {
        "total": len(manifest),
        "by_subset": dict(sorted(by_subset.items())),
        "by_language": dict(sorted(by_language.items())),
        "total_word_count": sum(int(entry.get("word_count", 0)) for entry in manifest),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_env_value(key: str) -> str | None:
    if os.environ.get(key):
        return os.environ[key]
    env_path = ROOT.parent.parent / ".env"
    if not env_path.exists():
        return None
    for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        value = line.strip()
        if not value or value.startswith("#") or "=" not in value:
            continue
        name, raw = value.split("=", 1)
        if name.strip() == key:
            return raw.strip().strip('"').strip("'")
    return None


if __name__ == "__main__":
    main()
