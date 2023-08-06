{ pkgs ? import <nixpkgs> { }
, py-ver ? 311
}:
let
  python-name = "python${toString py-ver}";
  python = builtins.getAttr python-name pkgs;
  python-pkgs = python.withPackages (p: with p; [ pytest ]);
in
pkgs.mkShell {
  buildInputs = [ python-pkgs ];
  shellHook = ''
    set -e
    PYTHONPATH="$(pwd)/src" python3 -m pytest -v unit_tests
    exit
  '';
}
