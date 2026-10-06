# split_notebook_heuristic.py
import nbformat, re
from nbformat import v4 as nbf
from pathlib import Path

IN = Path("major.ipynb")
OUT_PRE = Path("preprocessing.ipynb")
OUT_TRAIN = Path("training.ipynb")

nb = nbformat.read(str(IN), as_version=4)

pre_kw = re.compile(r'\b(preproc|pre-processing|preprocessing|data prep|tile|tiling|patch|augment|align|dataset|dataloader|mask remap|resize|crop)\b', re.I)
train_kw = re.compile(r'\b(train|training|epoch|optimizer|loss|model.train|checkpoint|scheduler|batch_size|num_epochs|backward|criterion|fit\(|validate)\b', re.I)
eval_kw  = re.compile(r'\b(eval|evaluate|inference|predict|miou|iou|f1|confusion|metric)\b', re.I)

pre_cells=[]
train_cells=[]
other_cells=[]
# collect top import block
imports=[]
for cell in nb.cells:
    if cell.cell_type=='code' and cell.source.strip().startswith(("import ","from ")):
        imports.append(cell)
    else:
        if imports:
            break

for cell in nb.cells:
    s = cell.source or ""
    l = s.lower()
    if cell.cell_type == 'markdown':
        if re.search(r'\b(preprocessing|data preparation|data pipeline)\b', l):
            pre_cells.append(cell); continue
        if re.search(r'\b(training|model training|training loop)\b', l):
            train_cells.append(cell); continue
    if cell.cell_type == 'code':
        if pre_kw.search(s) and not train_kw.search(s):
            pre_cells.append(cell); continue
        if train_kw.search(s) and not pre_kw.search(s):
            train_cells.append(cell); continue
        if eval_kw.search(s):
            other_cells.append(cell); continue
    # fallback heuristics
    if 'Dataset' in s or 'DataLoader' in s or 'albumentations' in s:
        pre_cells.append(cell)
    elif 'timm.create_model' in s or 'def forward' in s or 'nn.Module' in s or 'model =' in s:
        train_cells.append(cell)
    else:
        other_cells.append(cell)

pre_nb = nbf.new_notebook()
train_nb = nbf.new_notebook()
pre_nb.cells = [nbf.new_markdown_cell("# Preprocessing (auto-extracted)")] + imports + pre_cells
train_nb.cells = [nbf.new_markdown_cell("# Training (auto-extracted)")] + imports + train_cells

nbformat.write(pre_nb, str(OUT_PRE))
nbformat.write(train_nb, str(OUT_TRAIN))
print("Wrote:", OUT_PRE, OUT_TRAIN)
print("NOTE: please inspect both notebooks; some cells may need manual relocation.")
