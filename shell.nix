{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages(ps: [
    ps.black
    ps.mypy
  ]);

in pkgs.mkShell {
  buildInputs = [
    pythonEnv
  ];
}
