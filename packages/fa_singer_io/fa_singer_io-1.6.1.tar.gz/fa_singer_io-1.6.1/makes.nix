# https://github.com/fluidattacks/makes
{
  cache = {
    readAndWrite = {
      enable = true;
      name = "fa-foss";
      pubKey = "fa-foss.cachix.org-1:RoFAjJdHUUFrNAfbaLFqvFQVfmNmyMMAorl7j2VqV9M=";
    };
    readExtra = [
      {
        url = "https://fluidattacks.cachix.org";
        pubKey = "fluidattacks.cachix.org-1:zHq9yBCfg0wUPBDWdMFs62x6X/MJvSgGAWX8Vq9PnUY=";
      }
    ];
  };
  formatBash = {
    enable = true;
    targets = ["/"];
  };
  formatNix = {
    enable = true;
    targets = ["/"];
  };
  formatPython = {
    enable = true;
    targets = ["/"];
  };
  lintBash = {
    enable = true;
    targets = ["/"];
  };
  lintNix = {
    enable = true;
    targets = ["/"];
  };
}
