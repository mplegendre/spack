from spack import *

class Gdb(Package):
    """The GNU Debugger"""
    homepage = "https://www.gnu.org/software/gdb/"
    url      = "ftp://ftp.gnu.org/gnu/gdb/gdb-7.9.tar.gz"

    version('7.9', '8f8ced422fe462a00e0135a643544f17')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
