"""Extract the .fbx files of every Mixamo pack zip in Downloads into <work>/extract/<pack name>/."""
import glob, os, sys, zipfile
DL = 'C:/Users/Jame/Downloads'
work = sys.argv[1]
for z in sorted(glob.glob(DL + '/*Pack*.zip')):
    d = os.path.join(work, 'extract', os.path.splitext(os.path.basename(z))[0])
    with zipfile.ZipFile(z) as f:
        for i in f.infolist():
            if i.is_dir() or not i.filename.lower().endswith('.fbx'):
                continue
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, os.path.basename(i.filename)), 'wb').write(f.read(i))
print('extracted to', os.path.join(work, 'extract'))
