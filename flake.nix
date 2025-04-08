{
  description = "A Nix-flake development environment for robotic-arm ";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {
    # self,
    nixpkgs,
    ...
  }: let
    # system should match the system you are running on
    system = "x86_64-linux";
  in {
    devShells."${system}".default = let
      pkgs = import nixpkgs {
        inherit system;
      };
    in
      pkgs.mkShell rec {
        name = "impurePythonEnv";
        venvDir = "./.venv";

        buildInputs = with pkgs; [
          python3Packages.python
          python3Packages.venvShellHook

          python3Packages.bleak
          python3Packages.tkinter
          python3Packages.python-lsp-server
          python3Packages.python-lsp-ruff
          python3Packages.pylsp-rope

          (python3Packages.opencv4.override {
            enableGtk3 = true;
            enableGtk2 = false;
          })

          ruff
          mpremote
          rshell
        ];

        LD_LIBRARY_PATH = with pkgs;
          lib.makeLibraryPath ([
            ]
            ++ buildInputs);

        postVenvCreation = ''
          unset SOURCE_DATE_EPOCH
          pip install -r requirements.txt
        '';

        postShellHook = ''
          # allow pip to install wheels
          unset SOURCE_DATE_EPOCH
        '';
      };
  };
}
