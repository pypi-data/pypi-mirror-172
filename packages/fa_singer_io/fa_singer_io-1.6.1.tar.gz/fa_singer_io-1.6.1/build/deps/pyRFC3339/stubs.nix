lib:
lib.buildPythonPackage rec {
  pname = "types-pyRFC3339";
  version = "1.1.1";
  src = lib.fetchPypi {
    inherit pname version;
    hash = "sha256:jtJhc3rmpuPirxPWAYAZshU42MJ19GEnxYquy1axpY8=";
  };
}
