# Repository Agent Rules & Operational Constraints

## 1. Professional Document Generation (Typst / Markdown / PDF)

When generating or modifying reports, briefs, and documentation in this repository:
1. **No Hallucinations or Roleplay:** Never insert fake signature placeholders, fake government seals, or mock statutory audit certificates.
2. **Strict Sentence Case:** Use sentence case for all headings (e.g., "Total capital outlay", not "TOTAL CAPITAL OUTLAY" or "Total Capital Outlay") unless strictly instructed otherwise.
3. **High Density Layouts:** Do not pad pages with arbitrary whitespace to artificially increase page counts. Use multi-column layouts and precise grid fitting to maximize information density.
4. **No AI Slop:** Adhere strictly to objective, encyclopedic vocabulary. Avoid thematic breaks (`---`) to break up standard text sections unless logically necessary.

## 2. Tight Loop Performance Exception (Ponytail Override)

When auditing code for over-engineering or replacing "hand-rolled" logic with standard library or third-party dependencies (e.g., when applying `ponytail` principles):
1. **Context Matters:** Always check if the code executes inside a tight loop (e.g., >1,000 iterations per cycle).
2. **Instantiation Overhead:** Do not replace lightweight pure-Python math/geometry functions with heavy library objects (like `matplotlib.path.Path` or `numpy` class instantiations) inside tight loops if it introduces massive object-creation overhead.
3. **Execution Over Dogma:** The simplest code that runs fast is better than "clean" dependency code that hangs the pipeline.
