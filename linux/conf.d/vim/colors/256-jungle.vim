" Vim color file
" Maintainer:	Piotr Husiatyński <phusiatynski@gmail.com>

set background=dark
set t_Co=256
let g:colors_name="256-jungle"

let python_highlight_all = 1
let c_gnu = 1


hi Identifier	ctermfg=226         ctermbg=None        cterm=None
hi Normal	    ctermfg=229         ctermbg=None         cterm=None
hi Cursor       ctermfg=216         ctermbg=57          cterm=None
hi SpecialKey	ctermfg=70          ctermbg=None        cterm=None
hi Directory	ctermfg=57          ctermbg=254         cterm=None
hi ErrorMsg     ctermfg=160         ctermbg=245         cterm=None
hi PreProc	    ctermfg=83         ctermbg=None        cterm=None
hi Search	    ctermfg=125         ctermbg=255        cterm=Bold
hi Type		    ctermfg=157         ctermbg=None        cterm=None
hi Statement	ctermfg=159         ctermbg=None        cterm=None
hi Comment	    ctermfg=253         ctermbg=None        cterm=None
hi LineNr	    ctermfg=244         ctermbg=233         cterm=None
hi NonText	    ctermfg=105         ctermbg=None        cterm=Bold
hi DiffText	    ctermfg=165         ctermbg=244         cterm=None
hi Constant	    ctermfg=154          ctermbg=None        cterm=None
hi Todo         ctermfg=162         ctermbg=None        cterm=Bold
hi Error	    ctermfg=None        ctermbg=196         cterm=Bold
hi Special	    ctermfg=172         ctermbg=None        cterm=None
hi Ignore       ctermfg=221         ctermbg=None        cterm=Bold
hi Underline    ctermfg=147         ctermbg=None        cterm=Italic

hi FoldColumn	ctermfg=132         ctermbg=None        cterm=None
hi Folded       ctermfg=132         ctermbg=None        cterm=Bold

hi Visual       ctermfg=248         ctermbg=238         cterm=None

hi Pmenu        ctermfg=62          ctermbg=233         cterm=None
hi PmenuSel     ctermfg=69          ctermbg=232         cterm=Bold
hi PmenuSbar    ctermfg=247         ctermbg=233         cterm=Bold
hi PmenuThumb   ctermfg=248         ctermbg=233         cterm=None

hi StatusLineNC ctermfg=248         ctermbg=239         cterm=None
hi StatusLine   ctermfg=39          ctermbg=239         cterm=None
hi VertSplit    ctermfg=239         ctermbg=239         cterm=None

hi TabLine      ctermfg=245         ctermbg=239         cterm=None
hi TabLineFill  ctermfg=239         ctermbg=239
hi TabLineSel   ctermfg=104         ctermbg=236         cterm=Bold
