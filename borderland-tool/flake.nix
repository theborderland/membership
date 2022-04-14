{

  inputs = {
    # updated 2022-02-07
    nixpkgs = {
      type = "github";
      owner = "NixOS";
      repo = "nixpkgs";
      rev = "a102368ac4c3944978fecd9d7295a96d64586db5";
    };
  };


  outputs = { self, nixpkgs }: {

    packages.x86_64-linux.default = nixpkgs.legacyPackages.x86_64-linux.stdenv.mkDerivation {
      name = "example";
      buildInputs = [ 
        nixpkgs.legacyPackages.x86_64-linux.python3.withPackages (pkgs: with pkgs; [ certifi ])
      ];
      src = [
        ./borderland_tool
      ];
      unpackPhase = ''
        for file in $srcs; do
          cp -r $file $(stripHash $file)
        done
      '';
  };

}
