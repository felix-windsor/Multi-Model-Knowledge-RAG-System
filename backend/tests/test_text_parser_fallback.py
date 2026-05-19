from knowledge_graph_rag.parser import MineruParser


def test_mineru_parser_reads_markdown_text_without_cli(tmp_path):
    path = tmp_path / "sample.md"
    path.write_text("# 标题\n\n综合管理系统调用指标计算服务。", encoding="utf-8")

    content = MineruParser().parse_text_file(path)

    assert content == [
        {
            "type": "text",
            "text": "# 标题\n\n综合管理系统调用指标计算服务。",
            "page_idx": 0,
        }
    ]
