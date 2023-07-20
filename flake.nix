{
  description = "Flake template for a python project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        packageOverrides = pkgs.callPackage ./python-packages.nix { };
        python = pkgs.python39.override { inherit packageOverrides; };
        pythonWithPackages = python.withPackages (ps: [
          ps.certifi
          ps.charset-normalizer
          ps.icalendar
          ps.idna
          ps.python-dateutil
          ps.pythorhead
          ps.pytz
          ps.requests
          ps.six
          ps.urllib3
        ]);
      in with pkgs; {
        devShells.default = mkShell {
          buildInputs = [ pythonWithPackages ];
          packages = [  ];
        };
      });
}
