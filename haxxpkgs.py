from derivation import FixedOutputDerivation
from derivation import Derivation


class HelloSrc(FixedOutputDerivation):
    sha256 = "0fe1dc04f44edb96ff6d33411e7545650e7141386a827af2039199861aa78cb7"
    url = "https://raw.githubusercontent.com/rswier/c4/master/hello.c"


class Lololololol(Derivation):
    pname = "lolololololl"
    version = "0.1"
    src = HelloSrc
    build_inputs = []


class hello(Derivation):
    pname = "hello"
    version = "0.1"
    src = HelloSrc
    # build_inputs = []
    build_inputs = [ Lololololol ]
