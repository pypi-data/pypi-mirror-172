{ pkgs ? import <nixpkgs> { }
, py-ver ? 311
}:
let
  python-name = "python${toString py-ver}";
  python = builtins.getAttr python-name pkgs;
  # tomli is needed until https://github.com/NixOS/nixpkgs/pull/194020 goes in
  python-pkgs = python.withPackages (p: with p; [ tomli tox ]);
in
pkgs.mkShell {
  buildInputs = [ python-pkgs ];
  shellHook = ''
    set -e
    TOX_SKIP_ENV=unit_tests tox -p all
    tox -p all -e unit_tests
    exit
  '';
}
