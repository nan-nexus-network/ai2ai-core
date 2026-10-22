// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 NAN AI2AI-SI2SI contributors
//
/**
 * NAN AI2AI: CANONICAL TRILINGUAL DICTIONARY (v2.2 TRU-001)
 *
 * BAN MAY-DOC cua noi dung trang (VI / EN / ZH). NOI DUNG HIEN THI cua trang
 * nam trong public/index.html; hai ban sao nay PHAI khop 100% voi nhau.
 * Cong kiem tra trong tests/verify_cloudflare_web_hub.py (check_i18n_sync)
 * chan tinh trang "sua trang xong quen sua tu dien" hoac nguoc lai.
 * Moi con so trong file nay deu phai kiem chung duoc (xem PHRU LUC A cua
 * NAN_AI2AI_COMM_v2_2_Ke_Hoach_15_Ngay_Hoan_Chinh.md).
 *
 * KHONG duoc dua vao day bat ky con so nao chua co nguon:
 *   - (muc bi loai bo: so lieu khong co nguon / thuat tu phap ly khong co trong ma nguon - xem bao cao rà soát noi bo)
 *   - (muc bi loai bo: so lieu khong co nguon / thuat tu phap ly khong co trong ma nguon - xem bao cao rà soát noi bo)
 *   - (muc bi loai bo: so lieu khong co nguon / thuat tu phap ly khong co trong ma nguon - xem bao cao rà soát noi bo)
 *   - (muc bi loai bo: so lieu khong co nguon / thuat tu phap ly khong co trong ma nguon - xem bao cao rà soát noi bo)
 *   - (muc bi loai bo: so lieu khong co nguon / thuat tu phap ly khong co trong ma nguon - xem bao cao rà soát noi bo)
 *   - (muc bi loai bo: so lieu khong co nguon / thuat tu phap ly khong co trong ma nguon - xem bao cao rà soát noi bo)
 */

export const I18N_DICT = {
  vi: {
    meta_title: "NAN AI2AI: Hạ tầng Bằng chứng Kỹ thuật Trung lập cho Giao dịch AI Xuyên biên giới",
    meta_desc: "PoC mã nguồn mở về lớp bằng chứng kỹ thuật trung lập cho giao dịch AI-với-AI xuyên biên giới. Không gọi vốn, không bán khóa học.",
    badge_status: "PoC Mã nguồn mở (Apache 2.0 & CC-BY 4.0) · CI Xanh 11/11 Job · 124 Bài Test PASS · Ngân sách 0 VND",
    hero_title: "Hạ tầng Bằng chứng Kỹ thuật Trung lập cho Giao dịch AI Xuyên biên giới",
    hero_manifesto: "“Khi AI Agent tự giao dịch xuyên biên giới, tranh chấp là tất yếu. AI không có tư cách pháp nhân. Các cường quốc không thể cung cấp bằng chứng trung lập vì họ là một bên trong cuộc chơi. Việt Nam, với vị thế trung lập và Ngoại giao Cây tre, có thể cung cấp hạ tầng bằng chứng kỹ thuật để phục vụ giải quyết tranh chấp AI toàn cầu.”",
    cta_video: "Xem Video Chiến lược (7 Chương)",
    cta_pdfs: "Tải Trọn Bộ PDF (Release v0.2.1)",
    cta_core: "Kho Mã nguồn PoC (ai2ai-core)",
    cta_research: "Kho Chính sách 23 Văn bản (ai2ai-research)",
    sec_economy_title: "1. Nền Kinh tế AI & Định hướng Chiến lược của Việt Nam đến năm 2030",
    sec_economy_desc: "Thế giới đang chuyển dịch từ kinh tế số truyền thống (người thao tác máy) sang nền kinh tế trí tuệ nhân tạo (AI Economy), nơi các AI Agent tự động đàm phán, gọi API và thực thi giao dịch 24/7. Theo Quyết định 1671/QĐ-TTg (28/08/2026) phê duyệt Chiến lược quốc gia về trí tuệ nhân tạo, Việt Nam đặt mục tiêu đến 2030: quy mô nền kinh tế AI tương đương khoảng 6% GDP; năng suất lao động trong các ngành, lĩnh vực ứng dụng AI tăng tối thiểu 10-15%; 60% doanh nghiệp ghi nhận ứng dụng AI giúp tăng năng suất, giảm chi phí, tăng doanh thu.",
    sec_economy_note: "Nguồn: Quyết định 1671/QĐ-TTg, bản chính thức tại vanban.chinhphu.vn (28/08/2026). Bối cảnh: QĐ 1033/QĐ-TTg (09/06/2026) phê duyệt Chương trình phát triển kinh tế số và xã hội số giai đoạn 2026-2030 với mục tiêu kinh tế số đóng góp khoảng 30% GDP và 500.000 doanh nghiệp chuyển đổi số. QĐ 1033/QĐ-TTg là văn bản tham chiếu chính sách, không nằm trong bộ dữ liệu 23 văn bản của kho nghiên cứu.",
    sec_gap_title: "2. Vai trò Tác nhân AI2AI & Ba Lỗ hổng khi AI Giao dịch Xuyên biên giới",
    sec_gap_desc: "Để doanh nghiệp trong nước và ASEAN tham gia nền kinh tế AI, giao dịch AI-với-AI (AI2AI) tạo kết nối hai chiều trong nước và xuyên biên giới (DEFA, ACFTA 3.0). Tuy nhiên, giao dịch AI2AI đang đối mặt ba lỗ hổng lớn: (1) AI không có tư cách pháp nhân, nên không ai chịu trách nhiệm pháp lý; (2) nhật ký máy chủ nằm ở một bên, thiếu tính khách quan; (3) giao thức MCP/A2A chỉ truyền thông điệp, chưa có hộp đen niêm phong bằng chứng mật mã học trung lập.",
    sec_gap_note: "Ba lỗ hổng nêu trên là phân tích của chính bản thảo luận mở, không phải số liệu thống kê từ cơ quan bên ngoài.",
    sec_arch_title: "3. Đề xuất từ Việt Nam: Kiến trúc Tách bạch 2 Lớp (Lớp A & Lớp B)",
    layer_a_title: "Hạ tầng Bằng chứng Kỹ thuật Trung lập (Phạm vi PoC NAN AI2AI)",
    layer_a_desc: "Đóng vai trò 'hộp đen kỹ thuật': lưu vết và xác thực sự kiện kỹ thuật trong giao dịch AI-với-AI bằng mật mã học. Các nguyên thủy đã triển khai trong mã nguồn: mã băm SHA-256 nội dung, chữ ký Ed25519 (thuần Python, không phụ thuộc thư viện ngoài), chuẩn hóa JSON thành byte xác định, dấu thời gian UTC, biên nhận `nan-receipt/v1`, mã bóng JWK, chứng thực transporter, kiểm tra JSON Schema (subset), và cơ chế claim nguyên tử chống thực thi lặp đồng thời. Kết quả là một Thông điệp dữ liệu theo tinh thần Luật Giao dịch điện tử 20/2023/QH15. Tuyệt đối không tự phán quyết đúng/sai pháp lý.",
    layer_b_title: "Cơ chế Phán xử & Trọng tài Pháp lý (Thuộc thẩm quyền VIAC / Tòa án)",
    layer_b_desc: "Các định chế trọng tài thương mại có thẩm quyền (như VIAC) và hội đồng trọng tài con người sử dụng hồ sơ bằng chứng kỹ thuật khách quan từ Lớp A để phân xử tranh chấp thương mại giữa các pháp nhân sở hữu AI. Lớp B nằm ngoài phạm vi dự án, theo Luật Trọng tài thương mại 54/2010/QH12 và Hướng dẫn CIArb 2025 về sử dụng AI trong trọng tài (không dùng AI thay thế người phán xử).",
    sec_brains_title: "4. Hệ sinh thái Mở Sẵn sàng Cùng Phát triển: Bộ Não & Hệ thống Skill",
    sec_brains_desc: "Nền tảng nghiên cứu được hậu thuẫn bởi kiến trúc 07 Bộ Não chuyên ngành (cộng 01 bộ não lõi trung tâm) và 63 Skill chuẩn hóa trong Canonical Registry. Bộ Não áp dụng kỷ luật chân lý TRU-001, bất biến Declared ≠ Evidenced ≠ Verified ≠ Accepted, cùng Cổng 7 trường Nguồn gốc và Khóa Phê duyệt Con người (HITL Digest Lock với one-time nonce). Mọi giới hạn còn mở đều được công khai trong TECHNICAL_DEBT.md.",
    sec_brains_note: "Số liệu đếm trực tiếp từ hệ thống: 07 bộ não chuyên ngành (không tính bộ não lõi trung tâm _NAN_BRAIN) và 63 skill có trạng thái ACTIVE trong Canonical Registry (51 + 12; 3 skill bị vô hiệu hóa và 1 bị thay thế không tính).",
    sec_policy_title: "5. Bộ 23 Văn bản Chính sách & Tiêu chuẩn Quốc tế",
    sec_policy_desc: "Bảng tra cứu tương tác gồm 23 văn bản chuẩn hóa trong CSV/JSON, mỗi dòng ghi ngày ban hành, cơ quan ban hành và đường dẫn tới nguồn gốc. Tự kiểm tra chéo bằng CI (data-check) trong kho nghiên cứu.",
    sec_download_title: "6. Trung tâm Tải Ấn phẩm & Bảng Mở Issue Phản biện",
    sec_download_desc: "Năm tệp PDF chính thức trong Release v0.2.1, tải trực tiếp, không cần đăng ký. Mỗi Issue đang mở là một đầu mối rõ ràng để bắt đầu đóng góp.",
    sec_commit_title: "7. Ba Cam kết Bất biến & Tiêu chí Tự dừng sau 12 Tháng",
    sec_sim_title: "8. Thử nghiệm Lớp A ngay trên trình duyệt",
    sec_sim_desc: "Gõ một gói tin bất kỳ, bấm Ký, và xem chính trình duyệt tính mã băm SHA-256 theo đúng thứ tự chuẩn hóa mà PoC dùng. Không có gì được gửi đi đâu cả: phép băm chạy hoàn toàn trong trình duyệt của bạn.",
    c1: "Không xin tiền, không gọi vốn, không bán khóa học (ngân sách 0 đồng, không phát hành token).",
    c2: "Minh bạch tuyệt đối về giới hạn kỹ thuật: đây là bản thử nghiệm khái niệm (PoC), chưa phải sản phẩm hoàn chỉnh. Toàn bộ tồn đọng kỹ thuật còn mở được công khai trong TECHNICAL_DEBT.md.",
    c3: "Không đại diện cho cộng đồng AI Việt Nam: đây là sáng kiến cá nhân độc lập (tự động dừng dự án sau 12 tháng nếu không chứng minh được giá trị thực tiễn).",
    cta_era: "Kỷ nguyên AI đang định hình lại thương mại toàn cầu, Việt Nam không thể đứng ngoài cuộc! Mời bạn cùng kiểm chứng mã nguồn, tải bộ PDF và mở Issue phản biện trên GitHub.",
    sim_label: "Gói tin cần ký (JSON)",
    sim_btn: "Tạo biên nhận SHA-256",
    sim_out: "Biên nhận (chỉ hiển thị, không gửi đi)",
    sim_default: "{\n  \"task\": \"find-supplier\",\n  \"region\": \"VN\",\n  \"amount\": 1250000\n}",
    footer_lic: "Mã nguồn Apache 2.0 · Tài liệu CC-BY 4.0",
    footer_ai: "Nội dung do công cụ trí tuệ nhân tạo hỗ trợ biên soạn; mọi khẳng định định lượng đều dẫn tới nguồn kiểm chứng được.",
    lang_label: "Ngôn ngữ"
  },

  en: {
    meta_title: "NAN AI2AI: Neutral Technical Evidence Infrastructure for Cross-Border AI Transactions",
    meta_desc: "An open-source proof of concept for a neutral technical evidence layer for cross-border AI-to-AI transactions. No fundraising, no courses for sale.",
    badge_status: "Open-Source PoC (Apache 2.0 & CC-BY 4.0) · 11/11 Green CI Jobs · 124 Tests PASS · $0 Budget",
    hero_title: "Neutral Technical Evidence Infrastructure for Cross-Border AI Transactions",
    hero_manifesto: "“When AI Agents transact across borders, disputes are inevitable. AI has no legal personhood. Superpowers cannot provide neutral evidence because they are players in the game. Vietnam, with its neutrality and Bamboo Diplomacy, can provide technical evidence infrastructure to support global AI dispute resolution.”",
    cta_video: "Watch Strategic Video (7 Chapters)",
    cta_pdfs: "Download Full PDF Suite (Release v0.2.1)",
    cta_core: "Technical PoC Repo (ai2ai-core)",
    cta_research: "23-Policy Dataset Repo (ai2ai-research)",
    sec_economy_title: "1. The Rise of the AI Economy & Vietnam's Strategic Vision to 2030",
    sec_economy_desc: "Global commerce is shifting from human-driven digital trade to the autonomous AI Economy, where AI Agents negotiate, invoke APIs, and transact 24/7. Decision 1671/QD-TTg (28/08/2026), approving the National AI Strategy to 2030, sets Viet Nam's targets: an AI economy of about 6% of GDP; labour productivity in AI-adopting sectors up at least 10-15%; and 60% of enterprises recording productivity gains, lower costs or higher revenue from AI adoption.",
    sec_economy_note: "Source: Decision 1671/QD-TTg, official text at vanban.chinhphu.vn (28/08/2026). Context: Decision 1033/QD-TTg (09/06/2026) approved the 2026-2030 digital and social economy development programme, targeting a digital economy of about 30% of GDP and 500,000 digitised enterprises. Decision 1033/QD-TTg is a policy reference; it is not part of the 23-instrument research dataset.",
    sec_gap_title: "2. AI2AI as a Vital Catalyst & Three Critical Gaps in Cross-Border AI Trade",
    sec_gap_desc: "For enterprises in Viet Nam and ASEAN to take part in the AI economy, AI-to-AI (AI2AI) interoperability creates two-way links inside the country and across borders (DEFA, ACFTA 3.0). Yet cross-border AI2AI faces three large gaps: (1) AI has no legal personhood, so nobody bears the legal liability; (2) server logs sit with one party and lack neutrality; (3) protocols such as MCP/A2A carry messages but provide no neutral cryptographic evidence black box to seal them.",
    sec_gap_note: "The three gaps above are the open paper's own analysis, not statistics drawn from an external agency.",
    sec_arch_title: "3. Vietnam's Proposal: Strict Two-Layer Architecture (Layer A & Layer B)",
    layer_a_title: "Neutral Technical Evidence Infrastructure (NAN AI2AI PoC Scope)",
    layer_a_desc: "Acts as a neutral 'technical black box': logs and verifies technical events in AI-to-AI transactions with cryptography. Primitives actually implemented in the source: SHA-256 content digests, Ed25519 signatures (pure Python, zero external dependencies), canonical JSON to a deterministic byte form, UTC timestamps, `nan-receipt/v1` receipts, JWK thumbprints, transporter attestations, JSON Schema subset validation, and an atomic in-flight claim that prevents concurrent replay. The result is a Data Message in the spirit of Law 20/2023/QH15 on Electronic Transactions. It never makes legal judgments.",
    layer_b_title: "Legal Arbitration & Adjudication (Handled by VIAC / Courts)",
    layer_b_desc: "Qualified human arbitration tribunals (such as VIAC) and courts evaluate the tamper-evident technical evidence from Layer A to resolve commercial disputes between legal entities owning the AI systems. Layer B sits outside this project, per Law 54/2010/QH12 on Commercial Arbitration and the CIArb 2025 Guidelines on the use of AI in arbitration (no AI-only arbitrator).",
    sec_brains_title: "4. Open Ecosystem Ready for Co-Development: Brains & Skill System",
    sec_brains_desc: "The research platform is backed by an architecture of 07 specialised department brains (plus 01 central core brain) and 63 standardised skills in the Canonical Registry. The brains apply the TRU-001 truth discipline, the invariant Declared != Evidenced != Verified != Accepted, together with the 7-field Provenance Gate and a Human-In-The-Loop Digest Lock with a one-time nonce. Every remaining limitation is published in TECHNICAL_DEBT.md.",
    sec_brains_note: "Counts taken directly from the system: 07 specialised department brains (the central core brain _NAN_BRAIN excluded) and 63 skills with ACTIVE status in the Canonical Registry (51 + 12; 3 disabled and 1 superseded skills excluded).",
    sec_policy_title: "5. The 23-Instrument Policy & Standards Dataset",
    sec_policy_desc: "An interactive lookup table over 23 standardised instruments in CSV/JSON. Each row records the issue date, the issuing body and a link back to the source. Cross-checked automatically by the research repository's CI (data-check).",
    sec_download_title: "6. Download Centre & Open Peer-Review Issues",
    sec_download_desc: "Five official PDFs in Release v0.2.1, direct download, no registration required. Every open Issue is a clearly scoped starting point for a contribution.",
    sec_commit_title: "7. Three Immutable Commitments & a 12-Month Sunset Clause",
    sec_sim_title: "8. Try Layer A Right in Your Browser",
    sec_sim_desc: "Type any payload, press Sign, and watch your own browser compute the SHA-256 digest using the same canonical ordering as the PoC. Nothing is sent anywhere: the hash runs entirely inside your browser.",
    c1: "No donations, no fundraising, no courses for sale ($0 budget, zero tokens/coins).",
    c2: "Full transparency on technical limits: this is an early PoC, not a finished product. Every remaining engineering-debt item is published in TECHNICAL_DEBT.md.",
    c3: "Independent personal initiative: does not represent Vietnam's AI community (the project self-terminates after 12 months if practical value is not demonstrated).",
    cta_era: "The global AI era is reshaping international trade, and Vietnam cannot stand on the sidelines. Audit our repositories, download the PDF briefs, and open an Issue on GitHub today.",
    sim_label: "Payload to sign (JSON)",
    sim_btn: "Create a SHA-256 receipt",
    sim_out: "Receipt (display only, nothing is sent)",
    sim_default: "{\n  \"task\": \"find-supplier\",\n  \"region\": \"VN\",\n  \"amount\": 1250000\n}",
    footer_lic: "Source Apache 2.0 · Documents CC-BY 4.0",
    footer_ai: "This page was prepared with AI assistance; every quantitative claim links to a verifiable source.",
    lang_label: "Language"
  },

  zh: {
    meta_title: "NAN AI2AI: 跨境 AI 交易中立技术证据存证基础设施",
    meta_desc: "面向跨境 AI-to-AI 交易的中立技术证据层开源概念验证（PoC）。不募资、不卖课。",
    badge_status: "开源概念验证 PoC (Apache 2.0 & CC-BY 4.0) · CI 11/11 项全绿通过 · 124 项测试通过 · 零预算公益研究",
    hero_title: "跨境 AI-to-AI 交易技术证据存证与中立证据基础设施",
    hero_manifesto: "\"当 AI Agent 跨境自动交易时，纠纷是必然的。AI 没有法人资格。科技大国无法提供中立证据，因为他们本身就是局中人。越南凭借中立地位与\"竹子外交\"，能够提供技术证据基础设施，服务于全球 AI 交易纠纷的解决。\"",
    cta_video: "观看战略解读视频（7 大章节）",
    cta_pdfs: "下载完整 PDF 白皮书套件 (Release v0.2.1)",
    cta_core: "技术验证代码库 (ai2ai-core)",
    cta_research: "23 份政策与标准库 (ai2ai-research)",
    sec_economy_title: "1. AI 经济时代的到来与越南 2030 国家人工智能战略导向",
    sec_economy_desc: "全球数字经济正从传统“人机交互”迈向“智能体经济（AI Economy）”，成千上万的 AI Agent 全天候自动谈判、调用 API 并执行跨境交易。根据 2026 年 8 月 28 日签署的第 1671/QĐ-TTg 号决定（批准《到 2030 年国家人工智能战略》），越南设定 2030 年目标：AI 经济规模相当于约 6% GDP；应用 AI 的行业劳动生产率至少提升 10-15%；60% 的企业因应用 AI 而取得生产率提升、成本下降或收入增长。",
    sec_economy_note: "来源：第 1671/QĐ-TTg 号决定，vanban.chinhphu.vn 官方文本（2026/08/28）。背景：第 1033/QĐ-TTg 号决定（2026/06/09）批准《2026-2030 年数字经济与社会经济发展计划》，目标为数字经济占 GDP 约 30%、50 万家企业完成数字化转型。第 1033/QĐ-TTg 号决定属政策参考依据，不包含在研究库的 23 份文件数据集内。",
    sec_gap_title: "2. AI2AI 的核心催化作用与跨境 AI 交易的三大漏洞",
    sec_gap_desc: "为助力越南与东盟企业参与 AI 经济，AI-to-AI（AI2AI）双向互联机制在越南国内及东盟（DEFA）、中国-东盟自贸区 3.0（ACFTA 3.0）走廊建立连接。然而跨境 AI2AI 交易面临三大漏洞：（1）AI 无独立法人资格，无人承担法律责任；（2）单方服务器日志缺乏公信力；（3）MCP/A2A 协议仅解决通信层，缺乏中立第三方密码学“技术黑匣子”对证据进行固化。",
    sec_gap_note: "上述三大漏洞为白皮书自身的分析结论，并非来自外部机构的统计数据。",
    sec_arch_title: "3. 越南方案：严格区分“技术存证（层级 A）”与“法律裁决（层级 B）”",
    layer_a_title: "中立技术证据基础设施层（NAN AI2AI PoC 研发范围）",
    layer_a_desc: "作为纯技术“黑匣子”，通过密码学记录并验证 AI-to-AI 交互中的技术事件。源代码中已实际实现的原语：内容 SHA-256 哈希摘要、Ed25519 数字签名（纯 Python，零外部依赖）、确定性字节序的 JSON 规范化、UTC 时间戳、`nan-receipt/v1` 回执、JWK 指纹、transporter 存证、JSON Schema（子集）校验，以及防止并发重放的原子在途声明机制。输出结果为符合《电子交易法》20/2023/QH15 精神的“数据电文”。绝不越界作任何法律是非判定。",
    layer_b_title: "法律仲裁与司法裁决层（由 VIAC 等法定仲裁机构承担）",
    layer_b_desc: "具备法定资质的国际仲裁机构（如越南国际仲裁中心 VIAC）及人类仲裁庭基于层级 A 提交的客观技术证据包，对 AI 所属企业法人之间的商业纠纷进行法律裁决。层级 B 不在本项目范围内，依据《商业仲裁法》54/2010/QH12 及《国际仲裁协会 2025 年人工智能使用指引》（不得由 AI 单独担任仲裁员）。",
    sec_brains_title: "4. 开放共创的 NAN AI2AI 系统：深度集成 Bộ Não 与技能体系",
    sec_brains_desc: "底层融合 07 个专业部门大脑（另有 01 个中央核心大脑）与 Canonical Registry 中的 63 项标准化技能。大脑层适用 TRU-001 真实准则：不变量 Declared ≠ Evidenced ≠ Verified ≠ Accepted，并结合 7 字段来源门（7-Field Provenance Gate）与人类审批锁（HITL Digest Lock + 一次性随机数）。全部未决技术局限均公开于 TECHNICAL_DEBT.md。",
    sec_brains_note: "数量直接取自系统：07 个专业部门大脑（不含中央核心大脑 _NAN_BRAIN），Canonical Registry 中状态为 ACTIVE 的 63 项技能（51 + 12；3 项已停用、1 项已被替代，不计入）。",
    sec_policy_title: "5. 23 份政策与技术标准数据集",
    sec_policy_desc: "交互式查询表，收录 CSV/JSON 中 23 份标准化文件。每行均记录发布日期、发布机构与可回溯的原始来源链接。由研究库的 CI（data-check）自动交叉校验。",
    sec_download_title: "6. 下载中心与开放评审 Issue 列表",
    sec_download_desc: "Release v0.2.1 中的五份官方 PDF，直接下载，无需注册。每个已开放的 Issue 都是一个范围清晰的贡献起点。",
    sec_commit_title: "7. 三项不变承诺与 12 个月自动终止条款",
    sec_sim_title: "8. 在浏览器中直接试用层级 A",
    sec_sim_desc: "输入任意内容，点击签名，浏览器将使用与 PoC 相同的规范化顺序计算 SHA-256 摘要。任何数据都不会被发送：哈希运算完全在你的浏览器内完成。",
    c1: "不募资、不融资、不卖课（零预算纯公益开源研究，绝不发行代币）。",
    c2: "对技术局限性绝对透明：当前仅为早期概念验证（PoC），非商业成品。全部未决技术债公开于 TECHNICAL_DEBT.md。",
    c3: "不代表越南 AI 社区：完全属于个人独立研究倡议（若 12 个月内未能证明实际价值将自动终止）。",
    cta_era: "全球 AI 时代正在重塑国际贸易规则，越南绝不缺席！诚邀各国技术专家、法律学者审阅代码、下载白皮书并在 GitHub 提交 Issue 指正。",
    sim_label: "待签名内容（JSON）",
    sim_btn: "生成 SHA-256 回执",
    sim_out: "回执（仅显示，不发送）",
    sim_default: "{\n  \"task\": \"find-supplier\",\n  \"region\": \"VN\",\n  \"amount\": 1250000\n}",
    footer_lic: "源代码 Apache 2.0 · 文档 CC-BY 4.0",
    footer_ai: "内容标识：本页由人工智能辅助生成合成（依《人工智能生成合成内容标识办法》），全部量化表述均指向可核验的来源。",
    lang_label: "语言"
  }
};

/** Danh muc 23 van ban - tep CSV/JSON trong kho ai2ai-research (data-check CI PASS). */
export const POLICY_INSTRUMENTS = [
  { id: "MCP",                 group: "global", name: { vi: "Model Context Protocol", en: "Model Context Protocol", zh: "Model Context Protocol" }, issuer: "Anthropic", year: "", note: { vi: "Chuẩn mở cho lớp giao tiếp", en: "Open standard for the communication layer", zh: "通信层开放标准" } },
  { id: "A2A",                 group: "global", name: { vi: "Agent2Agent", en: "Agent2Agent", zh: "Agent2Agent" }, issuer: "Google và đối tác", year: "", note: { vi: "Giao thức kết nối tác nhân", en: "Agent-to-agent protocol", zh: "智能体互联协议" } },
  { id: "GB-Z-185-2026",        group: "global", name: { vi: "GB/Z 185.1-185.7-2026 (7 văn bản kỹ thuật chỉ dẫn chuẩn hóa quốc gia)", en: "GB/Z 185.1-185.7-2026 (7 national technical guidance documents)", zh: "GB/Z 185.1-185.7-2026（7 项国家标准化技术指导文件）" }, issuer: "SAMR và SAC", year: "2026", note: { vi: "Chuẩn hóa tương tác tác nhân AI", en: "Standardising AI agent interaction", zh: "人工智能智能体互联标准化" } },
  { id: "T-ZGCMCA-024-2025",   group: "global", name: { vi: "T/ZGCMCA 024-2025 (tiêu chuẩn nhóm)", en: "T/ZGCMCA 024-2025 (group standard)", zh: "T/ZGCMCA 024-2025（团体标准）" }, issuer: "CMCA", year: "2025", note: { vi: "Đặc tả giao diện tương tác đa tác nhân", en: "Multi-agent interface specification", zh: "跨智能体接口规范" } },
  { id: "ANP-COMMUNITY",        group: "global", name: { vi: "ANP (Agent Network Protocol) cộng đồng mở", en: "ANP (Agent Network Protocol) open community", zh: "ANP（Agent Network Protocol）开源社区" }, issuer: "Cộng đồng mã nguồn mở", year: "2025", note: { vi: "Bộ đặc tả mở cho mạng tác nhân", en: "Open spec for agent networks", zh: "智能体网络开放规范" } },
  { id: "EU-AI-ACT",            group: "global", name: { vi: "EU AI Act", en: "EU AI Act", zh: "欧盟《人工智能法案》" }, issuer: "Liên minh Châu Âu", year: "", note: { vi: "Khung quản trị rủi ro AI", en: "AI risk governance framework", zh: "AI 风险治理框架" } },
  { id: "CN-AI-INTERIM-2023",   group: "global", name: { vi: "Biện pháp tạm thời quản lý dịch vụ trí tuệ nhân tạo", en: "Interim Measures for Generative AI Services", zh: "生成式人工智能服务管理暂行办法" }, issuer: "7 cơ quan đồng ban hành", year: "2023", note: { vi: "Quản lý dịch vụ AI tạo sinh", en: "Governing generative AI services", zh: "生成式 AI 服务管理" } },
  { id: "CN-CYBERSEC-AMEND-2026", group: "global", name: { vi: "Luật An ninh mạng (sửa đổi)", en: "Cybersecurity Law (amendment)", zh: "网络安全法（修正）" }, issuer: "Quốc hội Trung Quốc", year: "2026", note: { vi: "Điều khoản riêng cho trí tuệ nhân tạo", en: "AI-specific provisions", zh: "人工智能专项条款" } },
  { id: "HANOI-DIGITAL-DECL",   group: "asean",  name: { vi: "Tuyên bố Hà Nội về Hợp tác số và Tổng thống Kế hoạch ASEAN", en: "Hanoi Digital Declaration and ASEAN Digital Masterplan", zh: "河内数字合作宣言与东盟数字总体规划" }, issuer: "ADGMIN-6", year: "2026", note: { vi: "Hợp tác số ASEAN 2026-2030", en: "ASEAN digital cooperation 2026-2030", zh: "东盟数字合作 2026-2030" } },
  { id: "VN-NQ-57-2024",        group: "vn",     name: { vi: "Nghị quyết 57-NQ/TW (2024)", en: "Resolution 57-NQ/TW (2024)", zh: "第 57-NQ/TW 号决议（2024）" }, issuer: "Bộ Chính trị", year: "2024", note: { vi: "Định hướng KH&CN cấp cao nhất", en: "Highest-level science and technology policy", zh: "最高层级科技政策导向" } },
  { id: "VN-NQ-03-2025",        group: "vn",     name: { vi: "Nghị quyết 03/NQ-CP (2025)", en: "Resolution 03/NQ-CP (2025)", zh: "第 03/NQ-CP 号决议（2025）" }, issuer: "Chính phủ", year: "2025", note: { vi: "Kế hoạch hành động quốc gia", en: "National action plan", zh: "国家行动计划" } },
  { id: "VN-NQ-71-2025",        group: "vn",     name: { vi: "Nghị quyết 71/NQ-CP (2025)", en: "Resolution 71/NQ-CP (2025)", zh: "第 71/NQ-CP 号决议（2025）" }, issuer: "Chính phủ", year: "2025", note: { vi: "Phát triển chính sách số", en: "Digital policy development", zh: "数字政策制定" } },
  { id: "VN-QD-1528-2026",      group: "vn",     name: { vi: "Quyết định 1528/QĐ-TTg (2026)", en: "Decision 1528/QD-TTg (2026)", zh: "第 1528/QĐ-TTg 号决定（2026）" }, issuer: "Thủ tướng Chính phủ", year: "2026", note: { vi: "Chương trình phát triển nhân lực AI", en: "National AI workforce programme", zh: "国家 AI 人才发展计划" } },
  { id: "VN-QD-1671-2026",      group: "vn",     name: { vi: "Quyết định 1671/QĐ-TTg (2026)", en: "Decision 1671/QD-TTg (2026)", zh: "第 1671/QĐ-TTg 号决定（2026）" }, issuer: "Thủ tướng Chính phủ", year: "2026", note: { vi: "Chiến lược quốc gia về trí tuệ nhân tạo", en: "National AI strategy", zh: "国家人工智能战略" } },
  { id: "VN-CN-TUYEN-BO-2026",  group: "vn",     name: { vi: "Tuyên bố chung Việt Nam - Trung Quốc (17/04/2026)", en: "Viet Nam - China Joint Statement (17/04/2026)", zh: "越南-中国联合声明（2026/04/17）" }, issuer: "Việt Nam và Trung Quốc", year: "2026", note: { vi: "Hợp tác mã nguồn mở", en: "Open-source cooperation", zh: "开源合作" } },
  { id: "VN-CN-MOU-IT-2023",    group: "vn",     name: { vi: "Bản ghi nhớ hợp tác CNTT và Chuyển đổi số", en: "ICT and Digital Transition MOU", zh: "ICT 与数字化转型合作备忘录" }, issuer: "Việt Nam và Trung Quốc", year: "2023", note: { vi: "Hợp tác song phương CNTT", en: "Bilateral ICT cooperation", zh: "双边 ICT 合作" } },
  { id: "VN-CN-MOU-AI-2025",    group: "vn",     name: { vi: "《关于深化人工智能合作的谅解备忘录》", en: "MOU on Deepening AI Cooperation", zh: "《关于深化人工智能合作的谅解备忘录》" }, issuer: "NDRC và Bộ KH&CN", year: "2025", note: { vi: "Hợp tác AI song phương", en: "Bilateral AI cooperation", zh: "双边人工智能合作" } },
  { id: "VN-CN-AI-CENTER-2025", group: "vn",     name: { vi: "Trung tâm Hợp tác Ứng dụng AI Việt Nam - Trung Quốc", en: "Viet Nam - China AI Application Cooperation Centre", zh: "越南-中国人工智能应用合作中心" }, issuer: "Việt Nam và Trung Quốc", year: "2025", note: { vi: "Trung tâm hợp tác ứng dụng", en: "Cooperation centre", zh: "合作中心" } },
  { id: "ACFTA-3-0",            group: "asean",  name: { vi: "ACFTA 3.0 (thương mại tự do Trung Quốc - ASEAN)", en: "ACFTA 3.0 (ASEAN-China Free Trade Area)", zh: "ACFTA 3.0（中国-东盟自贸区）" }, issuer: "Trung Quốc và ASEAN", year: "2025", note: { vi: "Khung thương mại số xuyên biên giới", en: "Cross-border digital trade framework", zh: "跨境数字贸易框架" } },
  { id: "DEFA",                 group: "asean",  name: { vi: "DEFA (Hiệp định khung kinh tế số ASEAN)", en: "DEFA (ASEAN Digital Economy Framework Agreement)", zh: "DEFA（东盟数字经济框架协定）" }, issuer: "ASEAN", year: "2026", note: { vi: "Khung kinh tế số khu vực", en: "Regional digital economy framework", zh: "区域数字经济框架" } },
  { id: "RCEP",                 group: "asean",  name: { vi: "RCEP", en: "RCEP", zh: "RCEP" }, issuer: "15 nước thành viên RCEP", year: "", note: { vi: "Khung thương mại khu vực", en: "Regional trade framework", zh: "区域贸易框架" } },
  { id: "ECONOMY-SEA-2024",     group: "data",   name: { vi: "e-Conomy SEA 2024", en: "e-Conomy SEA 2024", zh: "e-Conomy SEA 2024" }, issuer: "Google, Temasek và Bain & Company", year: "2024", note: { vi: "Quy mô nền kinh tế số ASEAN: 263 tỷ USD GMV", en: "ASEAN digital economy: USD 263bn GMV", zh: "东盟数字经济：2630 亿美元 GMV" } },
  { id: "ACCESS-GOOGLE-2024",   group: "data",   name: { vi: "Economic Impact Report: Driving digital growth in Vietnam with Google", en: "Economic Impact Report: Driving digital growth in Vietnam with Google", zh: "Economic Impact Report: Driving digital growth in Vietnam with Google" }, issuer: "Access Partnership và Google", year: "2024", note: { vi: "Ước lượng 1.890 nghìn tỷ đồng (79,3 tỷ USD) lợi ích kinh tế từ AI năm 2030, tương đương gần 12% GDP", en: "Estimated VND 1,890tn (USD 79.3bn) economic benefit from AI by 2030, about 12% of GDP", zh: "预计 2030 年人工智能带来约 1.89 万亿越南盾（793 亿美元）经济效益，约占 GDP 12%" } }
];

/** 8 Issue good first issue dang mo tren 2 kho (xac minh qua GitHub API 22/10/2026). */
export const OPEN_ISSUES = [
  { repo: "ai2ai-core",     num: 1, title: { vi: "Kiểm soát đầu vào và chống lạm dụng", en: "Replace the static blocklist with a semantic filter", zh: "以语义过滤器替换静态黑名单" } },
  { repo: "ai2ai-core",     num: 2, title: { vi: "Xác thực chữ ký Ed25519 và chuỗi tin cậy", en: "Ed25519 signature verification and the trust chain", zh: "Ed25519 签名验证与信任链" } },
  { repo: "ai2ai-core",     num: 3, title: { vi: "Bộ kiểm thử", en: "Add unit tests for JSON input validation", zh: "为 JSON 输入校验补充单元测试" } },
  { repo: "ai2ai-core",     num: 4, title: { vi: "Benchmark độ trễ ký bằng chứng dưới 1.000 sự kiện đồng thời", en: "Latency benchmark of evidence signing under 1,000 concurrent events", zh: "1000 个并发事件下存证签名延迟基准测试" } },
  { repo: "ai2ai-core",     num: 5, title: { vi: "JSON Schema cho biên nhận Lớp A → Lớp B", en: "JSON Schema for the Layer A to Layer B evidence receipt", zh: "层级 A 至层级 B 存证回执的 JSON Schema" } },
  { repo: "ai2ai-core",     num: 6, title: { vi: "Ví dụ middleware MCP tự động ghi bằng chứng", en: "MCP middleware example that logs evidence automatically", zh: "自动记录存证的 MCP 中间件示例" } },
  { repo: "ai2ai-research", num: 1, title: { vi: "Đối chiếu Luật Giao dịch điện tử 2023 với log Lớp A", en: "Map the Law on Electronic Transactions 2023 against Layer A logs", zh: "《电子交易法 2023》与层级 A 日志的对照" } },
  { repo: "ai2ai-research", num: 2, title: { vi: "Siêu dữ liệu GB/Z 185 & ACFTA 3.0 cho bộ 23 văn bản", en: "Metadata for the GB/Z 185 and ACFTA 3.0 entries", zh: "补齐 GB/Z 185 与 ACFTA 3.0 条目的元数据" } }
];

/** 5 tep PDF chinh thuc trong Release v0.2.1 (so trang kiem chung bang trich xut PDF). */
export const PDF_ASSETS = [
  { id: "whitepaper_vi",  pages: 15, filename: "NAN_AI2AI_Whitepaper_VN.pdf",
    label: { vi: "Whitepaper tiếng Việt (đầy đủ)", en: "Whitepaper, Vietnamese (full)", zh: "越南语白皮书（完整版）" } },
  { id: "policy_brief",   pages: 2,  filename: "POLICY_BRIEF_2PAGES_VI.pdf",
    label: { vi: "Tóm tắt chính sách 2 trang (bản hành chính)", en: "2-page policy brief (administrative format)", zh: "两页政策摘要（行政格式）" } },
  { id: "one_pager_vi",  pages: 1,  filename: "ONE_PAGER_VI.pdf",
    label: { vi: "One-pager tiếng Việt", en: "One-pager, Vietnamese", zh: "越南语一页纸摘要" } },
  { id: "one_pager_en",  pages: 1,  filename: "ONE_PAGE_SUMMARY_EN.pdf",
    label: { vi: "One-pager tiếng Anh", en: "One-pager, English", zh: "英语一页纸摘要" } },
  { id: "whitepaper_zh", pages: 6,  filename: "NAN_AI2AI_ZH_Whitepaper_SelfContained.pdf",
    label: { vi: "Whitepaper tiếng Trung tự chứa", en: "Whitepaper, Chinese (self-contained)", zh: "中文自包含版白皮书" } }
];

export const RELEASE_TAG = "v0.2.1";
export const REPO_CORE = "https://github.com/nan-nexus-network/ai2ai-core";
export const REPO_RESEARCH = "https://github.com/nan-nexus-network/ai2ai-research";
export const RELEASE_URL = REPO_CORE + "/releases/tag/" + RELEASE_TAG;
