When using remote files, using the remote path will be slow, but you do not want to manually download to the local. You can use this library to automatically download management cache files, but still use the original remote path.

For example:

from pathcache import pathcachestr as pc

open(pc(r"/mnt/smb_01/xxx/yy/z.txt"))

This will create ./_pathcache/mnt/smb_01/xxx/yy/z.txt copy from /mnt/smb_01/xxx/yy/z.txt

Actully, the argument to the open() is str absolute path of "./_pathcache/mnt/smb_01/xxx/yy/z.txt"