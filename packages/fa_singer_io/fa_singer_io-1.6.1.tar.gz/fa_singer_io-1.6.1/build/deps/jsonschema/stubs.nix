lib:
lib.buildPythonPackage rec {
  pname = "types-jsonschema";
  version = "4.4.1";
  src = lib.fetchPypi {
    inherit pname version;
    hash = "sha256:vWi3UhfruzOwJC2xAEdYHa07BhqWOkbugNSpBECAZj4=";
  };
}
