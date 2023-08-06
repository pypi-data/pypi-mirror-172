{
  nixpkgs,
  python_version,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
  };
  python_pkgs = nixpkgs."${python_version}Packages";
  final_pkgs =
    python_pkgs
    // {
      fa-purity = nixpkgs.purity."${python_version}".pkg;
      import-linter = import ./import-linter {
        inherit lib;
        click = python_pkgs.click;
        networkx = python_pkgs.networkx;
      };
      jsonschema = python_pkgs.jsonschema.overridePythonAttrs (
        old: rec {
          version = "3.2.0";
          SETUPTOOLS_SCM_PRETEND_VERSION = version;
          src = lib.fetchPypi {
            inherit version;
            pname = old.pname;
            sha256 = "yKhbKNN3zHc35G4tnytPRO48Dh3qxr9G3e/HGH0weXo=";
          };
        }
      );
      types-jsonschema = import ./jsonschema/stubs.nix lib;
      types-pyRFC3339 = import ./pyRFC3339/stubs.nix lib;
    };
in {
  inherit lib;
  python_pkgs = final_pkgs;
}
