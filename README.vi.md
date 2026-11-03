<div align="center">

# 🔬 Agent Research Kit

**Template nghiên cứu chuẩn mực, tái lập được và tích hợp sẵn AI-agent — cho nghiên cứu học thuật & khoa học dữ liệu.**

Clone về, chạy một câu lệnh là bắt đầu nghiên cứu ngay — với cấu trúc dự án gọn
gàng, khả năng tái lập (reproducibility) tích hợp sẵn, khung bài báo LaTeX, và
các skill cho agent cài sẵn, dùng ngay làm dự án [OpenResearch](https://github.com/tuandang304/OpenResearch).

[![CI](https://github.com/tuandang304/research-template/actions/workflows/ci.yml/badge.svg)](https://github.com/tuandang304/research-template/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Use this template](https://img.shields.io/badge/use%20this-template-2ea44f?logo=github)](https://github.com/tuandang304/research-template/generate)

[English](README.md) · [Tiếng Việt](README.vi.md)

</div>

---

## Vì sao nên dùng template này?

Phần lớn code nghiên cứu bắt đầu từ một notebook lộn xộn và không bao giờ gọn lại
được. Template này cho bạn một **bộ khung chuyên nghiệp ngay từ ngày đầu**, giúp
công việc luôn tái lập được, dễ chia sẻ và dễ chuyển thành bài báo.

- 🧪 **Tái lập mặc định** — một nơi cấu hình duy nhất, một lệnh seed mọi bộ sinh số ngẫu nhiên.
- 📁 **Cấu trúc hợp lý** — `data/ · notebooks/ · experiments/ · results/ · paper/`.
- 📦 **Chạy được ngay** — `uv sync` cài đủ mọi thứ; có sẵn một thí nghiệm mẫu chạy thật.
- 📄 **Sẵn sàng viết báo** — khung LaTeX lấy hình trực tiếp từ `results/`, kèm `CITATION.cff`.
- 🤖 **Sẵn sàng cho AI-agent** — có hướng dẫn `AGENTS.md` và các skill cho trích dẫn, tài liệu thiết kế, bộ nhớ dự án.
- ✅ **Đầy đủ công cụ** — test, linting (ruff), CI, và mẫu issue/PR đã cấu hình sẵn.

## Bắt đầu nhanh (Quickstart)

> Cần [**uv**](https://docs.astral.sh/uv/) (khuyến khích) hoặc `pip` thông thường.

```bash
# 1. Lấy code (hoặc bấm "Use this template" trên GitHub)
git clone https://github.com/tuandang304/research-template.git
cd research-template

# 2. Cài mọi thứ vào một môi trường độc lập
uv sync                     # phiên bản khoá trong uv.lock, đã gồm công cụ dev. --extra notebook cho Jupyter

# 3. Chạy thí nghiệm trong config.yaml — huấn luyện mô hình, in một dòng summary,
#    ghi results/metrics.json và lưu hình vào results/figures/
uv run python main.py
```

Thích dùng pip? `python -m venv .venv && source .venv/bin/activate && pip install -e ".[notebook]" ruff pytest`

Vậy là xong — bạn đã có một dự án nghiên cứu hoạt động và tái lập được.

## Dùng với OpenResearch

Template được thiết kế để làm dự án [OpenResearch](https://github.com/tuandang304/OpenResearch)
ngay từ đầu:

1. Trong `orx up`, tạo dự án mới và dán URL repo này làm repo để clone (hoặc tự
   `git clone` rồi import thư mục).
2. Đặt run command một lần: `orx project edit <projectId> --run-command 'uv run python main.py'`.
3. Tạo node baseline và chạy. Mọi node con giữ nguyên lệnh đó, chỉ đổi `config.yaml`
   hoặc code trên branch của chính nó.
4. Muốn có biểu đồ metric cạnh mỗi run thì `uv add trackio` (hoặc `uv sync --extra tracking`).
   `ark.start_run` đã dùng sẵn các biến `ORX_*` và `TRACKIO_PROJECT` mà orx đặt, nên
   `orx metrics <runId>` tìm được run. Không có Trackio thì dòng `summary:` trong log
   và file `results/metrics.json` vẫn ghi lại kết quả.

Agent đọc [AGENTS.md](AGENTS.md) (Claude Code đọc nó qua `CLAUDE.md`).

## Cấu trúc dự án

```
research-template/
├── src/ark/                # Package tái sử dụng của bạn (config, seed, logging, data IO, tracking)
├── experiments/            # Các module thí nghiệm, mỗi module có run(params)
├── notebooks/              # Khám phá dữ liệu; 01_exploratory.ipynb đã nối với `ark`
├── data/                   # raw / processed / external  (nội dung bị git bỏ qua)
├── results/                # figures / tables            (tự sinh lại, git bỏ qua)
├── paper/                  # Khung LaTeX + references.bib → dùng results/figures
├── docs/                   # Ghi chú thiết kế, tài liệu dữ liệu, nhật ký thí nghiệm
├── tests/                  # Test kiểm tra nhanh bằng pytest
├── config.yaml             # Config duy nhất: seed, thí nghiệm cần chạy, tham số của nó
├── main.py                 # Run command cố định:  uv run python main.py [info]
├── AGENTS.md · CLAUDE.md   # Hướng dẫn cho coding agent
├── .agents/skills/         # Các skill agent cài sẵn (xem bên dưới)
├── pyproject.toml          # Metadata, dependencies, cấu hình ruff & pytest
└── uv.lock                 # Phiên bản chính xác của dependencies — hãy commit
```

## Quy ước tái lập (Reproducibility)

Mọi thí nghiệm đều theo cùng các quy tắc, nên kết quả rất dễ tái lập:

```python
from ark import config, set_seed, start_run


def run(params):
    set_seed(config.seed)  # 1. Seed Python, NumPy và PyTorch (nếu có cài)
    with start_run("my_exp", params) as tracker:  # 2. Theo dõi metric (Trackio nếu có cài)
        ...  # 3. Đọc cấu hình từ params (config.yaml) — không hard-code
        tracker.summary({"accuracy": 0.93})  # 4. Một dòng summary cuối + results/metrics.json
```

Trỏ `experiment:` trong `config.yaml` tới module của bạn, rồi `uv run python main.py` sẽ chạy nó.
Dependencies được khoá trong `uv.lock`; thêm mới bằng `uv add <package>`.

Đường dẫn được phân giải từ thư mục gốc repo qua `ark.config`, nên cùng một đoạn
code chạy được từ script, notebook hay test — không phải mò `../../`.

## Từ thí nghiệm đến bài báo

Hình lưu vào `results/figures/` được `paper/main.tex` nạp trực tiếp
(`\graphicspath{{../results/figures/}}`). Biên dịch bài báo bằng `latexmk -pdf main.tex`
hoặc đưa thư mục lên [Overleaf](https://overleaf.com). GitHub cũng sẽ hiện nút
**"Cite this repository"** nhờ `CITATION.cff`.
## Các skill agent tích hợp sẵn 🤖

Một vài skill nghiên cứu nằm trong `.agents/skills/`, nơi Codex, OpenCode và các
agent đọc thư mục này sẽ tự nạp:

| Skill | Giúp bạn… |
| --- | --- |
| **bibtex-citation** | Lấy và định dạng BibTeX chuẩn cho `paper/references.bib`. |
| **system-design** | Soạn tài liệu kiến trúc và thiết kế cho `docs/`. |
| **memory-management** | Trao cho agent bộ nhớ dự án bền vững. |

Trong OpenResearch, mỗi phiên còn có thêm các skill `orx-*` của orx. Không dùng
agent? Thư mục này vô hại — xóa đi cũng không sao.


## Tùy biến cho riêng bạn

Sau khi bấm **Use this template**, hãy biến nó thành của bạn:

1. Đổi tên package `src/ark/` → `src/<tên_dự_án>` và cập nhật `pyproject.toml`.
2. Điền thông tin tác giả trong `pyproject.toml`, `LICENSE` và `CITATION.cff`.
3. Thêm dependencies bằng `uv add <package>` (cập nhật `uv.lock`).
4. Xóa thí nghiệm mẫu và những phần `paper/`/`.agents/` bạn không cần.

## Đóng góp

Rất hoan nghênh issue và PR — xem [CONTRIBUTING.md](CONTRIBUTING.md). Nếu template
này giúp bạn tiết kiệm thời gian, một ⭐ sẽ giúp người khác tìm thấy nó!

## Giấy phép

[MIT](LICENSE) — miễn phí cho cả mục đích học thuật và thương mại.
