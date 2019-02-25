wang:
	@python app.py wang
	pandoc -i output/wang.html -o output/wang.pdf --latex-engine=xelatex --template=data/default.latex
	pandoc -i output/wang.html -o output/wang.tex --latex-engine=xelatex --template=data/default.latex


sagart:
	@python app.py sagart
	pandoc -i output/sagart.html -o output/sagart.pdf --latex-engine=xelatex --template=data/default.latex
	pandoc -i output/sagart.html -o output/sagart.tex --latex-engine=xelatex --template=data/default.latex

pan:
	@python app.py pan
	pandoc -i output/pan.html -o output/pan.pdf --latex-engine=xelatex --template=data/default.latex
	pandoc -i output/pan.html -o output/pan.tex --latex-engine=xelatex --template=data/default.latex

gabelentz:
	@python app.py gabelentz
	pandoc -i output/gabelentz.html -o output/gabelentz.tex --latex-engine=xelatex --template=data/default.latex
	pandoc -i output/gabelentz.html -o output/gabelentz.pdf --latex-engine=xelatex --template=data/default.latex

haudricourt:
	@python app.py haudricourt
	pandoc -i output/haudricourt.html -o output/haudricourt.pdf --latex-engine=xelatex --template=data/default.latex
	pandoc -i output/haudricourt.html -o output/haudricourt.tex --latex-engine=xelatex --template=data/default.latex

pulleyblank:
	@python app.py pulleyblank
	pandoc -i output/pulleyblank.html -o output/pulleyblank.pdf --latex-engine=xelatex --template=data/default.latex
	pandoc -i output/pulleyblank.html -o output/pulleyblank.tex --latex-engine=xelatex --template=data/default.latex

starostin:
	@python app.py starostin
	pandoc -i output/starostin.html -o output/starostin.pdf --latex-engine=xelatex --template=data/default.latex
	pandoc -i output/starostin.html -o output/starostin.tex --latex-engine=xelatex --template=data/default.latex

all: sagart pan gabelentz haudricourt pulleyblank starostin wang

