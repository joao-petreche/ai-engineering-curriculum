#!/usr/bin/env python3
"""Build LaTeX artifacts from CURRICULUM_VALIDATION_REPORT.md.

This script generates manuscript.tex and references.bib from the current
repository layout, using relative paths by default.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SOURCE = BASE_DIR / "CURRICULUM_VALIDATION_REPORT.md"
DEFAULT_TEX = BASE_DIR / "manuscript.tex"
DEFAULT_BIB = BASE_DIR / "references.bib"

TITLE_FALLBACK = (
    "Validating the Scientific AI Engineering Curriculum: "
    "A Comprehensive Review of PIML, Interoperability, and Pedagogy (2024--2026)"
)
AUTHOR = "Scientific AI Engineering Research Group"
DATE = "2026"
KEYWORDS = (
    "Physics-Informed Machine Learning, Graph Neural Networks, "
    "Building Performance Simulation, Large Language Models, "
    "Simulation Interoperability, Physics-Constrained Safety, "
    "Training-First Pedagogy, Federated Learning"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--tex", type=Path, default=DEFAULT_TEX)
    parser.add_argument("--bib", type=Path, default=DEFAULT_BIB)
    return parser.parse_args()


def normalize_punctuation(text: str) -> str:
    replacements = {
        "\u2013": "--",
        "\u2014": "---",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2212": "-",
        "\u2192": "->",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u2206": "Delta",
        "\u03bb": "lambda",
        "\u2082": "2",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def fix_known_inline_citation_glitches(text: str) -> str:
    text = re.sub(r"\(\(\(([^()]+?,\s*\d{4}[a-z]?)\),\s*\d{4}[a-z]?\)\)", r"(\1)", text)
    text = re.sub(r"\(\(([^()]+?,\s*\d{4}[a-z]?)\),\s*\d{4}[a-z]?\)", r"(\1)", text)
    return text


def split_body_and_references(raw: str) -> tuple[str, str]:
    parts = re.split(r"^##\s*7\.\s*References\s*$", raw, maxsplit=1, flags=re.MULTILINE)
    if len(parts) != 2:
        raise ValueError("Could not find '## 7. References' section in source markdown")
    return parts[0].rstrip() + "\n", parts[1].strip() + "\n"


def extract_title(body_md: str) -> str:
    match = re.search(r"^#\s+(.+)$", body_md, flags=re.MULTILINE)
    if not match:
        return TITLE_FALLBACK
    return normalize_punctuation(match.group(1)).strip()


def parse_reference_items(refs_md: str) -> list[str]:
    items: list[str] = []
    current: list[str] = []
    for raw_line in refs_md.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            if current:
                items.append(" ".join(part.strip() for part in current).strip())
                current = []
            continue
        if line.lstrip().startswith("- "):
            if current:
                items.append(" ".join(part.strip() for part in current).strip())
            current = [line.lstrip()[2:].strip()]
            continue
        if current:
            current.append(line.strip())
    if current:
        items.append(" ".join(part.strip() for part in current).strip())
    return items


def cited_reference_numbers(body_md: str) -> list[int]:
    numbers: set[int] = set()
    for match in re.finditer(r"\[(\d+(?:\s*[-,]\s*\d+)*)\]", body_md):
        chunk = match.group(1)
        pieces = [part.strip() for part in chunk.split(",")]
        for piece in pieces:
            range_match = re.fullmatch(r"(\d+)\s*[-]\s*(\d+)", piece)
            if range_match:
                start = int(range_match.group(1))
                end = int(range_match.group(2))
                if start <= end:
                    numbers.update(range(start, end + 1))
                continue
            if piece.isdigit():
                numbers.add(int(piece))
    return sorted(numbers)


def split_reference_parts(item: str) -> tuple[str, str, str, str, str]:
    item = normalize_punctuation(item)
    doi_match = re.search(r"https?://doi\.org/(\S+)", item, flags=re.IGNORECASE)
    doi = doi_match.group(1).rstrip(".,)") if doi_match else ""
    year_match = re.search(r"\((\d{4}[a-z]?)\)", item, flags=re.IGNORECASE)
    year = year_match.group(1) if year_match else "2026"
    before_year = (
        re.split(r"\s*\(\d{4}[a-z]?\)", item, maxsplit=1)[0].strip().rstrip(".")
    )
    after_year_parts = re.split(r"\)\.\s*", item, maxsplit=1)
    after_year = after_year_parts[1].strip() if len(after_year_parts) > 1 else ""

    title = "Untitled"
    venue = ""
    title_match = re.match(
        r"(.+?)(?:\.\s+(?:In\s+)?\*|\.\s*\[|\.\s+https?://|$)", after_year
    )
    if title_match:
        title = title_match.group(1).strip().rstrip(".")
    venue_match = re.search(r"\*([^*]+)\*", after_year)
    if venue_match:
        venue = venue_match.group(1).strip()

    return before_year, title, year, venue, doi


def latex_escape(text: str) -> str:
    text = normalize_punctuation(text)
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("#", r"\#"),
        ("$", r"\$"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\^{}"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def bibtex_author_field(authors_raw: str) -> str:
    authors_raw = normalize_punctuation(authors_raw).strip().rstrip(".")
    return re.sub(r"\s*&\s*", " and ", authors_raw)


def make_reference_entry(index: int, item: str) -> str:
    authors_raw, title, year, venue, doi = split_reference_parts(item)
    fields = [
        f"@misc{{ref{index},",
        f"  author = {{{bibtex_author_field(authors_raw)}}},",
        f"  title = {{{latex_escape(title)}}},",
        f"  year = {{{year[:4]}}},",
    ]
    if venue:
        fields.append(f"  howpublished = {{{latex_escape(venue)}}},")
    if doi:
        fields.append(f"  url = {{https://doi.org/{doi}}},")
    fields.append(f"  note = {{{latex_escape(item)}}}")
    fields.append("}")
    return "\n".join(fields)


def make_placeholder_entry(index: int) -> str:
    return "\n".join(
        [
            f"@misc{{ref{index},",
            f"  author = {{{{Placeholder Reference {index}}}}},",
            f"  title = {{{latex_escape(f'Reference {index} (metadata pending validation)')}}},",
            "  year = {2026},",
            "  note = {Placeholder entry generated because the source markdown cites this reference number but does not define it in the References section.}",
            "}",
        ]
    )


def build_bibliography(body_md: str, refs_md: str) -> tuple[str, int, int]:
    items = parse_reference_items(refs_md)
    cited_numbers = cited_reference_numbers(body_md)
    max_needed = max(cited_numbers) if cited_numbers else len(items)
    entry_count = max(len(items), max_needed)

    entries = []
    for index in range(1, entry_count + 1):
        if index <= len(items):
            entries.append(make_reference_entry(index, items[index - 1]))
        else:
            entries.append(make_placeholder_entry(index))

    header = [
        "% Auto-generated by build_latex.py",
        "% Real references are mapped in source order to ref1..refN.",
        "% Missing cited references receive placeholders so manuscript.tex remains compilable.",
        "",
    ]
    placeholder_count = max(0, entry_count - len(items))
    return (
        "\n".join(header) + "\n\n".join(entries) + "\n",
        len(items),
        placeholder_count,
    )


def expand_numeric_chunk(chunk: str) -> list[int]:
    values: list[int] = []
    for piece in [part.strip() for part in chunk.split(",")]:
        range_match = re.fullmatch(r"(\d+)\s*[-]\s*(\d+)", piece)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            if start <= end:
                values.extend(range(start, end + 1))
            continue
        if piece.isdigit():
            values.append(int(piece))
    return values


def convert_numeric_citations(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        numbers = expand_numeric_chunk(match.group(1))
        keys = ",".join(f"ref{number}" for number in numbers)
        return rf"\cite{{{keys}}}"

    return re.sub(r"\[(\d+(?:\s*[-,]\s*\d+)*)\]", repl, text)


def strip_heading_prefix(text: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)*\.?\s*", "", text).strip()


def apply_inline_markdown(text: str) -> str:
    text = re.sub(r"`([^`]+)`", lambda m: rf"\texttt{{{m.group(1)}}}", text)
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: rf"\textbf{{{m.group(1)}}}", text)
    text = re.sub(
        r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)",
        lambda m: rf"\textit{{{m.group(1)}}}",
        text,
    )
    return text


def render_text(text: str) -> str:
    tokens: dict[str, str] = {}

    def stash(value: str, prefix: str) -> str:
        token = f"@@{prefix}{len(tokens)}@@"
        tokens[token] = value
        return token

    text = normalize_punctuation(text)
    text = fix_known_inline_citation_glitches(text)
    text = convert_numeric_citations(text)
    text = re.sub(r"\\cite\{[^}]+\}", lambda m: stash(m.group(0), "CITE"), text)
    text = latex_escape(text)
    text = apply_inline_markdown(text)
    for token, value in tokens.items():
        text = text.replace(token, value)
    return text.strip()


def md_to_latex_body(body_md: str) -> str:
    lines = body_md.splitlines()
    out: list[str] = []
    in_enumerate = False
    in_itemize = False
    in_abstract = False
    skip_toc = False

    def close_lists() -> None:
        nonlocal in_enumerate, in_itemize
        if in_enumerate:
            out.append(r"\end{enumerate}")
            in_enumerate = False
        if in_itemize:
            out.append(r"\end{itemize}")
            in_itemize = False

    def close_abstract() -> None:
        nonlocal in_abstract
        if in_abstract:
            out.append(r"\end{abstract}")
            in_abstract = False

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("# "):
            continue
        if stripped in {"---", "***", "___"}:
            close_lists()
            continue
        if stripped == "## Table of Contents":
            close_lists()
            close_abstract()
            skip_toc = True
            continue
        if skip_toc:
            if stripped.startswith("## ") and stripped != "## Table of Contents":
                skip_toc = False
            else:
                continue

        if stripped == "## Abstract":
            close_lists()
            close_abstract()
            out.append(r"\begin{abstract}")
            in_abstract = True
            continue
        if stripped.startswith("## "):
            close_lists()
            close_abstract()
            out.append(
                rf"\section{{{render_text(strip_heading_prefix(stripped[3:]))}}}"
            )
            continue
        if stripped.startswith("### "):
            close_lists()
            out.append(
                rf"\subsection{{{render_text(strip_heading_prefix(stripped[4:]))}}}"
            )
            continue
        if stripped.startswith("#### "):
            close_lists()
            out.append(
                rf"\subsubsection{{{render_text(strip_heading_prefix(stripped[5:]))}}}"
            )
            continue
        if not stripped:
            close_lists()
            out.append("")
            continue
        if re.match(r"^\d+\.\s+", stripped):
            if not in_enumerate:
                close_lists()
                out.append(r"\begin{enumerate}")
                in_enumerate = True
            item_text = re.sub(r"^\d+\.\s+", "", stripped)
            out.append(rf"  \item {render_text(item_text)}")
            continue
        if re.match(r"^[-*]\s+", stripped):
            if not in_itemize:
                close_lists()
                out.append(r"\begin{itemize}")
                in_itemize = True
            item_text = re.sub(r"^[-*]\s+", "", stripped)
            out.append(rf"  \item {render_text(item_text)}")
            continue

        close_lists()
        out.append(render_text(stripped))

    close_lists()
    close_abstract()
    return "\n".join(out).strip() + "\n"


def build_preamble(title: str) -> str:
    return f"""\\documentclass[12pt,a4paper]{{article}}

%% ------ Encoding & fonts ------------------------------------------------------------------------
\\usepackage[T1]{{fontenc}}
\\usepackage[utf8]{{inputenc}}

%% ------ Page layout -----------------------------------------------------------------------------
\\usepackage[top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm,headheight=14pt]{{geometry}}
\\usepackage{{setspace}}
\\doublespacing

%% ------ Typography -----------------------------------------------------------------------------
\\usepackage[protrusion=true,expansion=false]{{microtype}}
\\usepackage{{parskip}}
\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{6pt plus 2pt minus 1pt}}

%% ------ Section formatting ----------------------------------------------------------------------
\\usepackage{{titlesec}}
\\titleformat{{\\section}}{{\\large\\bfseries}}{{\\thesection.}}{{0.5em}}{{}}
\\titleformat{{\\subsection}}{{\\normalsize\\bfseries}}{{\\thesubsection}}{{0.5em}}{{}}
\\titleformat{{\\subsubsection}}{{\\normalsize\\itshape}}{{\\thesubsubsection}}{{0.5em}}{{}}

%% ------ Headers & footers -----------------------------------------------------------------------
\\usepackage{{fancyhdr}}
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyhead[L]{{\\small\\textit{{Scientific AI Engineering Curriculum Review}}}}
\\fancyhead[R]{{\\small\\thepage}}
\\renewcommand{{\\headrulewidth}}{{0.4pt}}

%% ------ Line numbers ----------------------------------------------------------------------------
\\usepackage{{lineno}}
\\linenumbers

%% ------ Colours ---------------------------------------------------------------------------------
\\usepackage[dvipsnames,table]{{xcolor}}
\\definecolor{{linkblue}}{{RGB}}{{0,70,127}}

%% ------ Hyperlinks ------------------------------------------------------------------------------
\\usepackage[
  colorlinks=true,
  linkcolor=linkblue,
  citecolor=linkblue,
  urlcolor=linkblue,
  pdftitle={{{latex_escape(title)}}},
  pdfauthor={{{latex_escape(AUTHOR)}}},
  pdfkeywords={{{latex_escape(KEYWORDS)}}},
  bookmarks=true
]{{hyperref}}

%% ------ Bibliography ----------------------------------------------------------------------------
\\usepackage[numbers,sort&compress]{{natbib}}

%% ------ Lists -----------------------------------------------------------------------------------
\\usepackage{{enumitem}}
\\setlist[itemize]{{noitemsep,topsep=4pt}}
\\setlist[enumerate]{{noitemsep,topsep=4pt}}

%% ------ Misc ------------------------------------------------------------------------------------
\\usepackage{{booktabs}}
\\usepackage{{caption}}
\\usepackage{{graphicx}}
\\usepackage{{amsmath,amssymb}}

%% ------ Abstract formatting ---------------------------------------------------------------------
\\renewenvironment{{abstract}}{{%
  \\vspace{{8pt}}
  \\noindent\\rule{{\\linewidth}}{{0.4pt}}\\vspace{{4pt}}
  \\noindent{{\\bfseries Abstract.}}\\quad\\itshape}}
  {{\\par\\vspace{{4pt}}\\noindent\\rule{{\\linewidth}}{{0.4pt}}\\vspace{{8pt}}}}

\\begin{{document}}

\\title{{\\textbf{{{latex_escape(title)}}}}}
\\author{{{latex_escape(AUTHOR)}}}
\\date{{{DATE}}}
\\maketitle
\\thispagestyle{{fancy}}
"""


def build_document(title: str, body_latex: str) -> str:
    tail = r"""

%% ------ References ------------------------------------------------------------------------------
\bibliographystyle{plainnat}
\bibliography{references}

\end{document}
"""
    return build_preamble(title) + "\n" + body_latex + tail


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    tex_path = args.tex.resolve()
    bib_path = args.bib.resolve()

    if not source.exists():
        raise FileNotFoundError(f"Source markdown not found: {source}")

    raw = normalize_punctuation(source.read_text(encoding="utf-8"))
    body_md, refs_md = split_body_and_references(raw)
    title = extract_title(body_md)

    body_latex = md_to_latex_body(body_md)
    bib_content, real_count, placeholder_count = build_bibliography(body_md, refs_md)
    document = build_document(title, body_latex)

    tex_path.write_text(document, encoding="utf-8")
    bib_path.write_text(bib_content, encoding="utf-8")

    print(f"Wrote LaTeX manuscript: {tex_path}")
    print(f"Wrote bibliography: {bib_path}")
    print(f"Mapped real references: {real_count}")
    print(f"Generated placeholders: {placeholder_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
