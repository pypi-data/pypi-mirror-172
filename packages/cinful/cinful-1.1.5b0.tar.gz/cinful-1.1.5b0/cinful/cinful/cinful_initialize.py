import subprocess

def main():
    print('Running conda package installer for cinful..')
    subprocess.run(["mamba", "env", "update", "--file", "cinful_conda.yml"])
    print('Installing pip packages..')
    subprocess.run(["pip", "install", "pyTMHMM==1.3.2"])
    subprocess.run(["pip", "install", "seqhash==1.0.0"])
    subprocess.run(["pip", "install", "blake3==0.2.0"])
    subprocess.run(["pip", "install", "cinful"])
    print('Environment setup complete for cinful')
    print('Please read log above to determine if setup succeded')
    print('Run \'cinful -h\' to verify successful installation')

if __name__ == "__main__":
    main()
