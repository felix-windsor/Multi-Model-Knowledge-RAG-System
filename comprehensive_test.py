"""
多模态知识图谱RAG系统综合测试
测试内容：
1. 文档上传和解析性能
2. 局部查询模式 (local)
3. 全局查询模式 (global)
4. 混合查询模式 (hybrid/mix)
"""
import httpx
import time
import json
from pathlib import Path
from datetime import datetime
import sys

class RAGSystemTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = {
            "test_time": datetime.now().isoformat(),
            "document_processing": {},
            "query_tests": {
                "local": [],
                "global": [],
                "hybrid": [],
                "mix": []
            },
            "issues": [],
            "observations": []
        }

    def log(self, message, level="INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "[INFO]",
            "SUCCESS": "[SUCCESS]",
            "ERROR": "[ERROR]",
            "WARNING": "[WARNING]"
        }.get(level, "[INFO]")
        print(f"{timestamp} {prefix} {message}")

    def add_observation(self, observation):
        """添加观察记录"""
        self.test_results["observations"].append({
            "time": datetime.now().isoformat(),
            "note": observation
        })

    def add_issue(self, issue, severity="medium"):
        """添加问题记录"""
        self.test_results["issues"].append({
            "time": datetime.now().isoformat(),
            "severity": severity,
            "description": issue
        })

    def test_upload_document(self, pdf_path):
        """测试文档上传和解析"""
        self.log("="*60)
        self.log("开始文档上传和解析测试")
        self.log("="*60)

        if not Path(pdf_path).exists():
            self.log(f"文件不存在: {pdf_path}", "ERROR")
            self.add_issue(f"测试文件不存在: {pdf_path}", "high")
            return None

        file_size = Path(pdf_path).stat().st_size / 1024  # KB
        self.log(f"文件大小: {file_size:.2f} KB")

        start_time = time.time()

        try:
            with httpx.Client(timeout=300.0) as client:
                with open(pdf_path, 'rb') as f:
                    files = {'file': (Path(pdf_path).name, f, 'application/pdf')}

                    self.log("正在上传文件...")
                    upload_start = time.time()
                    response = client.post(f"{self.base_url}/api/upload", files=files)
                    upload_time = time.time() - upload_start

                    if response.status_code == 200:
                        result = response.json()
                        doc_id = result.get('document_id')

                        self.log(f"文件上传成功! Document ID: {doc_id}", "SUCCESS")
                        self.log(f"上传耗时: {upload_time:.2f}秒")

                        # 监控文档处理进度
                        self.log("\n开始监控文档处理进度...")
                        processing_start = time.time()
                        max_wait = 300  # 最多等待5分钟
                        check_interval = 2  # 每2秒检查一次

                        while True:
                            if time.time() - processing_start > max_wait:
                                self.log("文档处理超时", "ERROR")
                                self.add_issue("文档处理超过5分钟仍未完成", "high")
                                break

                            status_resp = client.get(f"{self.base_url}/api/documents/{doc_id}")
                            if status_resp.status_code == 200:
                                status_data = status_resp.json()
                                status = status_data.get('status')

                                elapsed = time.time() - processing_start
                                self.log(f"[{elapsed:.1f}s] 处理状态: {status}")

                                if status == 'completed':
                                    processing_time = time.time() - processing_start
                                    total_time = time.time() - start_time

                                    self.log(f"\n文档处理完成!", "SUCCESS")
                                    self.log(f"解析耗时: {processing_time:.2f}秒")
                                    self.log(f"总耗时: {total_time:.2f}秒")
                                    self.log(f"平均速度: {file_size/processing_time:.2f} KB/s")

                                    # 记录结果
                                    self.test_results["document_processing"] = {
                                        "document_id": doc_id,
                                        "file_name": Path(pdf_path).name,
                                        "file_size_kb": file_size,
                                        "upload_time": upload_time,
                                        "processing_time": processing_time,
                                        "total_time": total_time,
                                        "speed_kb_per_sec": file_size/processing_time,
                                        "status": "success"
                                    }

                                    # 性能评估
                                    if processing_time > 60:
                                        self.add_observation(f"文档处理时间较长: {processing_time:.2f}秒")
                                    if file_size/processing_time < 10:
                                        self.add_observation(f"处理速度较慢: {file_size/processing_time:.2f} KB/s")

                                    return doc_id

                                elif status == 'failed':
                                    error_msg = status_data.get('error', 'Unknown error')
                                    self.log(f"文档处理失败: {error_msg}", "ERROR")
                                    self.add_issue(f"文档处理失败: {error_msg}", "high")
                                    self.test_results["document_processing"] = {
                                        "status": "failed",
                                        "error": error_msg
                                    }
                                    return None

                            time.sleep(check_interval)

                    else:
                        self.log(f"文件上传失败: {response.status_code}", "ERROR")
                        self.log(f"响应内容: {response.text}", "ERROR")
                        self.add_issue(f"文件上传失败: HTTP {response.status_code}", "high")
                        return None

        except Exception as e:
            self.log(f"上传过程出错: {e}", "ERROR")
            self.add_issue(f"上传过程异常: {str(e)}", "high")
            import traceback
            traceback.print_exc()
            return None

    def test_query(self, question, mode, doc_id=None):
        """测试知识查询"""
        self.log(f"\n测试查询 [{mode}模式]: {question}")

        payload = {
            "question": question,
            "mode": mode
        }
        if doc_id:
            payload["doc_ids"] = [doc_id]

        try:
            with httpx.Client(timeout=60.0) as client:
                start_time = time.time()
                response = client.post(f"{self.base_url}/api/query", json=payload)
                query_time = time.time() - start_time

                if response.status_code == 200:
                    result = response.json()
                    answer = result.get('answer', '')

                    self.log(f"查询成功! 耗时: {query_time:.2f}秒", "SUCCESS")
                    self.log(f"回答长度: {len(answer)} 字符")
                    self.log(f"回答预览: {answer[:200]}...")

                    # 记录结果
                    query_result = {
                        "question": question,
                        "mode": mode,
                        "query_time": query_time,
                        "answer_length": len(answer),
                        "answer": answer,
                        "status": "success"
                    }
                    self.test_results["query_tests"][mode].append(query_result)

                    # 性能评估
                    if query_time > 10:
                        self.add_observation(f"{mode}模式查询耗时较长: {query_time:.2f}秒")
                    if len(answer) < 50:
                        self.add_observation(f"{mode}模式回答较短: {len(answer)}字符，可能信息不足")

                    return answer
                else:
                    self.log(f"查询失败: {response.status_code}", "ERROR")
                    self.log(f"响应: {response.text}", "ERROR")
                    self.add_issue(f"{mode}模式查询失败: HTTP {response.status_code}", "medium")
                    return None

        except Exception as e:
            self.log(f"查询出错: {e}", "ERROR")
            self.add_issue(f"{mode}模式查询异常: {str(e)}", "medium")
            return None

    def run_comprehensive_test(self, pdf_path):
        """运行完整测试"""
        self.log("\n" + "="*60)
        self.log("多模态知识图谱RAG系统综合测试")
        self.log("="*60 + "\n")

        # 1. 文档上传和解析测试
        doc_id = self.test_upload_document(pdf_path)
        if not doc_id:
            self.log("文档上传失败，终止测试", "ERROR")
            return self.test_results

        # 等待一下确保处理完成
        time.sleep(3)

        # 2. 准备测试问题
        test_questions = [
            "这篇论文的主要贡献是什么？",
            "论文中提出了哪些关键技术或方法？",
            "实验结果如何？有哪些性能指标？",
            "这项研究有什么局限性或未来工作方向？"
        ]

        # 3. 测试局部查询模式
        self.log("\n" + "="*60)
        self.log("测试局部查询模式 (Local)")
        self.log("="*60)
        for q in test_questions[:2]:  # 测试前两个问题
            self.test_query(q, "local", doc_id)
            time.sleep(2)

        # 4. 测试全局查询模式
        self.log("\n" + "="*60)
        self.log("测试全局查询模式 (Global)")
        self.log("="*60)
        for q in test_questions[:2]:
            self.test_query(q, "global", doc_id)
            time.sleep(2)

        # 5. 测试混合查询模式
        self.log("\n" + "="*60)
        self.log("测试混合查询模式 (Hybrid)")
        self.log("="*60)
        for q in test_questions[:2]:
            self.test_query(q, "hybrid", doc_id)
            time.sleep(2)

        # 6. 测试Mix模式
        self.log("\n" + "="*60)
        self.log("测试Mix查询模式")
        self.log("="*60)
        for q in test_questions[:2]:
            self.test_query(q, "mix", doc_id)
            time.sleep(2)

        return self.test_results

    def generate_report(self, output_dir):
        """生成测试报告"""
        self.log("\n" + "="*60)
        self.log("生成测试报告")
        self.log("="*60)

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 生成Markdown报告
        report_file = output_path / "测试报告.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 多模态知识图谱RAG系统测试报告\n\n")
            f.write(f"**测试时间**: {self.test_results['test_time']}\n\n")

            # 文档处理结果
            f.write("## 1. 文档处理性能测试\n\n")
            doc_proc = self.test_results["document_processing"]
            if doc_proc.get("status") == "success":
                f.write("### 测试结果\n\n")
                f.write(f"- **文件名**: {doc_proc['file_name']}\n")
                f.write(f"- **文件大小**: {doc_proc['file_size_kb']:.2f} KB\n")
                f.write(f"- **上传耗时**: {doc_proc['upload_time']:.2f} 秒\n")
                f.write(f"- **解析耗时**: {doc_proc['processing_time']:.2f} 秒\n")
                f.write(f"- **总耗时**: {doc_proc['total_time']:.2f} 秒\n")
                f.write(f"- **处理速度**: {doc_proc['speed_kb_per_sec']:.2f} KB/s\n")
                f.write(f"- **状态**: ✅ 成功\n\n")
            else:
                f.write(f"### ❌ 处理失败\n\n")
                f.write(f"**错误**: {doc_proc.get('error', 'Unknown')}\n\n")

            # 查询测试结果
            f.write("## 2. 知识查询测试\n\n")

            modes = ["local", "global", "hybrid", "mix"]
            mode_names = {
                "local": "局部查询模式",
                "global": "全局查询模式",
                "hybrid": "混合查询模式",
                "mix": "Mix模式"
            }

            for mode in modes:
                queries = self.test_results["query_tests"].get(mode, [])
                if queries:
                    f.write(f"### 2.{modes.index(mode)+1} {mode_names[mode]}\n\n")

                    for i, q in enumerate(queries, 1):
                        f.write(f"#### 问题 {i}: {q['question']}\n\n")
                        f.write(f"- **耗时**: {q['query_time']:.2f} 秒\n")
                        f.write(f"- **回答长度**: {q['answer_length']} 字符\n")
                        f.write(f"- **状态**: {'✅ 成功' if q['status'] == 'success' else '❌ 失败'}\n\n")
                        f.write(f"**回答**:\n\n```\n{q['answer']}\n```\n\n")

            # 性能对比
            f.write("## 3. 不同查询模式性能对比\n\n")
            f.write("| 查询模式 | 平均耗时(秒) | 测试次数 |\n")
            f.write("|---------|------------|----------|\n")

            for mode in modes:
                queries = self.test_results["query_tests"].get(mode, [])
                if queries:
                    avg_time = sum(q['query_time'] for q in queries) / len(queries)
                    f.write(f"| {mode_names[mode]} | {avg_time:.2f} | {len(queries)} |\n")
            f.write("\n")

            # 问题和观察
            f.write("## 4. 问题记录\n\n")
            if self.test_results["issues"]:
                for issue in self.test_results["issues"]:
                    severity_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(issue["severity"], "⚪")
                    f.write(f"- {severity_icon} **[{issue['severity'].upper()}]** {issue['description']}\n")
            else:
                f.write("✅ 无重大问题\n")
            f.write("\n")

            f.write("## 5. 观察和建议\n\n")
            if self.test_results["observations"]:
                for obs in self.test_results["observations"]:
                    f.write(f"- {obs['note']}\n")
            else:
                f.write("无特殊观察\n")
            f.write("\n")

            # 总结
            f.write("## 6. 总结\n\n")
            doc_success = doc_proc.get("status") == "success"
            query_success = sum(len(q) for q in self.test_results["query_tests"].values()) > 0

            if doc_success and query_success:
                f.write("✅ 系统整体运行正常，文档处理和查询功能均可用。\n\n")
            else:
                f.write("⚠️ 系统存在部分功能问题，需要进一步优化。\n\n")

            # 优化建议
            f.write("### 优化建议\n\n")
            if doc_proc.get("processing_time", 0) > 60:
                f.write("1. 文档处理时间较长，建议优化解析算法或增加并行处理\n")

            all_queries = []
            for queries in self.test_results["query_tests"].values():
                all_queries.extend(queries)
            if all_queries:
                avg_query_time = sum(q['query_time'] for q in all_queries) / len(all_queries)
                if avg_query_time > 10:
                    f.write("2. 查询响应时间较长，建议优化检索算法或增加缓存\n")

            if len(self.test_results["issues"]) > 3:
                f.write("3. 发现多个问题，建议进行系统性排查和优化\n")

        # 保存JSON格式的详细数据
        json_file = output_path / "测试数据.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)

        self.log(f"测试报告已生成: {report_file}", "SUCCESS")
        self.log(f"详细数据已保存: {json_file}", "SUCCESS")

        return report_file


def main():
    # 测试配置
    pdf_path = "D:\\code_projects\\Multi-Model-Knowledge-RAG-System\\backend\\tests\\2209.07527v2.pdf"
    output_dir = "D:\\code_projects\\Multi-Model-Knowledge-RAG-System\\backend\\rethink\\第一次解析优化后测试"

    # 创建测试器
    tester = RAGSystemTester()

    # 运行测试
    results = tester.run_comprehensive_test(pdf_path)

    # 生成报告
    report_path = tester.generate_report(output_dir)

    print("\n" + "="*60)
    print("测试完成！")
    print(f"报告位置: {report_path}")
    print("="*60)

if __name__ == "__main__":
    main()
