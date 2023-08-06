# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady — Development shell
# :Created:   gio 30 giu 2022, 8:29:40
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2022 Lele Gaifax
#

{
  description = "metapensiero.sqlalchemy.dbloady";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      # Use the same nixpkgs
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, gitignore }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (builtins) fromTOML getAttr listToAttrs map readFile replaceStrings;
        pkgs = import nixpkgs { inherit system; };
        inherit (pkgs.lib) cartesianProductOfSets;
        inherit (gitignore.lib) gitignoreFilterWith;

        getSource = name: path: pkgs.lib.cleanSourceWith {
          name = name;
          src = path;
          filter = gitignoreFilterWith { basePath = path; };
        };

        pyVersions = ["python39" "python310"];
        saVersions = [
          { version = "1.3.24";
            sha256 = "ebbb777cbf9312359b897bf81ba00dae0f5cb69fba2a18265dcc18a6f5ef7519"; }
          { version = "1.4.42";
            sha256 = "177e41914c476ed1e1b77fd05966ea88c094053e17a85303c4ce007f88eff363"; }
          { version = "2.0.0b1";
            sha256 = "c811094ed523371c05f2257b5842aa185ffb27965931c65e3247e17d434c01f1"; }];

        mkSAPkg = python: saVersion: python.pkgs.buildPythonPackage rec {
          pname = "SQLAlchemy";
          version = saVersion.version;
          src = python.pkgs.fetchPypi {
            inherit pname version;
            sha256 = saVersion.sha256;
          };
          doCheck = false;
          nativeBuildInputs = [ python.pkgs.cython ];
          propagatedBuildInputs = [
            python.pkgs.greenlet
            python.pkgs.typing-extensions
          ];
        };

        mkDBLoadyApp = py: saVersion:
          let
            sqlalchemy' = mkSAPkg py saVersion;
          in
            py.pkgs.buildPythonPackage {
              pname = "dbloady";
              version = (fromTOML (readFile ./pyproject.toml)).project.version;
              format = "pyproject";
              src = getSource "dbloady" ./.;
              doCheck = false;
              nativeBuildInputs = [
                py.pkgs.pdm-pep517
              ];
              propagatedBuildInputs = with py.pkgs; [
                progressbar2
                ruamel-yaml
                sqlalchemy'
              ];
            };

        mkTestShell = pyVersion: saVersion:
          let
            py = getAttr pyVersion pkgs;
            dbloady = mkDBLoadyApp py saVersion;
            env = py.buildEnv.override {
              extraLibs = [
                dbloady
                py.pkgs.tomli
              ];
            };
          in pkgs.mkShell {
            name = "py-${py.version}+sa-${saVersion.version}";
            packages = with pkgs; [
              gnumake
              just
              postgresql_14

              env
            ];

            shellHook = ''
               TOP_DIR=$(pwd)
               trap "$TOP_DIR/tests/postgresql stop" EXIT
             '';
          };

        testsMatrix = cartesianProductOfSets { pyv = pyVersions; sav = saVersions; };
        allTestShells = map (combo: mkTestShell combo.pyv combo.sav) testsMatrix;
        testShells = listToAttrs (map (s: {
          name = replaceStrings ["."] ["_"] s.name;
          value = s;
        }) allTestShells);
      in {
        devShells = {
          default = pkgs.mkShell {
            name = "Dev shell";

            packages = (with pkgs; [
              bump2version
              gnumake
              just
              postgresql_14
              python3
              sqlite
              twine
            ]) ++ (with pkgs.python3Packages; [
              build
              progressbar2
              psycopg2
              ruamel-yaml
              sqlalchemy
              tomli
            ]);

            shellHook = ''
               TOP_DIR=$(pwd)
               export PYTHONPATH="$TOP_DIR/src''${PYTHONPATH:+:}$PYTHONPATH"
               trap "$TOP_DIR/tests/postgresql stop" EXIT
             '';
          };
        } // testShells;
      });
}
