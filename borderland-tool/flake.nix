{

  inputs = {
    # updated 2022-03-31
    nixpkgs = {
      type = "github";
      owner = "NixOS";
      repo = "nixpkgs";
      rev = "9bc841fec1c0e8b9772afa29f934d2c7ce57da8e";
    };
  };


  outputs = { self, nixpkgs }: {

    packages.x86_64-linux.default = nixpkgs.legacyPackages.x86_64-linux.stdenv.mkDerivation {
      name = "borderland-tool";
      buildInputs = [ 
        (nixpkgs.legacyPackages.x86_64-linux.python3.withPackages (pkgs: with pkgs; [ certifi chardet dateutils idna python-dateutil pytz requests six urllib3 ]))
      ];
      src = [
        ./borderland_tool
        ./setup.py
      ];
      unpackPhase = ''
        for file in $srcs; do
          cp -r $file $(stripHash $file)
        done
      '';
    };

  };

}
