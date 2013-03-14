if !has('python')
  echo "Error: Required vim compiled with +python"
  finish
endif

let g:FirefoxSyncRoot=expand("<sfile>:p:h")

autocmd CursorHold * call Timer()
function! Timer()
  call feedkeys("f\e")
endfunction

function! FirefoxSync()
python << EOF
import vim
import threading

root = vim.eval("g:FirefoxSyncRoot")
sys.path.append(root  + '/../libs/')

from fxui import MozUI
from client import MozClient

try:
    client = MozClient("localhost", 6000)


    ui = MozUI(client)
    tab = ui.getSelectedTab()
    ss = tab.getStyleSheets()
    s = ss[0];
    source = s.getSource()

    s.pushSource("*{background:red}", True)

    # vim.current.buffer is the current buffer. It's list-like object.
    # each line is an item in the list. We can loop through them delete
    # them, alter them etc.
    # Here we delete all lines in the current buffer
    del vim.current.buffer[:]

    # Here we append some lines above. Aesthetics.

    #vim.eval(":set filetype=css")
    vim.command("set filetype=css")
    vim.current.buffer.append(str(source).split('\n'), 0)

except Exception, e:
    print e
EOF
" Here the python code is closed. We can continue writing VimL or python again.
endfunction
