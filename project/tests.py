
def main():
    import subprocess

    fontsize = 10
    fontstyle = "Regular"
    font = "Monospace"
    font = f"URxvt.font: xft:{font}:style={fontstyle}:size={fontsize}"

    subprocess.run("cp /home/abdelmoumen/DEV-TESTS/PYTHON-PROJECTS/GUI_admin_tool/project/terminal/Xresources ~/.Xresources",shell=True)
    with open('~/.Xresources', mode='a') as file:
        file.write(f'\n{font}')
    subprocess.run("xrdb ~/.Xresources",shell=True)

if __name__ == '__main__':
    main()