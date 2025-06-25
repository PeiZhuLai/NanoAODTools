import uproot
import os
from pdb import set_trace

# 年份到输入目录的映射
year_dir_map = {
    "2016": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/UltraLegacy/",
    "2017": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PileUp/UltraLegacy/",
    "2018": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PileUp/UltraLegacy/",
    "2022preEE": "/eos/user/c/cmsdqm/www/CAF/certification/Collisions22/PileUp/BCD/",
    "2022postEE": "/eos/user/c/cmsdqm/www/CAF/certification/Collisions22/PileUp/EFG/",
    "2023preBPix": "/eos/user/c/cmsdqm/www/CAF/certification/Collisions23/PileUp/BC/",
    "2023postBPix": "/eos/user/c/cmsdqm/www/CAF/certification/Collisions23/PileUp/D/"
}

# 年份到era映射
year_era_map = {
    "2016": {
        "2016preVFP": "2016-preVFP",
        "2016postVFP": "2016-postVFP"
    },
    "2017": {
        "2017": "2017"
    },
    "2018": {
        "2018": "2018"
    },
    "2022preEE": {
        "2022preEE": "eraBCD"
    },
    "2022postEE": {
        "2022postEE": "eraEFG"
    },
    "2023preBPix": {
        "2023preBPix": "eraBC"
    },
    "2023postBPix": {
        "2023postBPix": "eraD"
    }
}

# 文件名与输出名映射
file_map = {
    "692": "pileup",
    "660": "pileup_plus",
    "724": "pileup_minus"
}

outfile = "99bins_withVar.root"

for year, indir in year_dir_map.items():
    era_map = year_era_map[year]
    root_files = [f for f in os.listdir(indir) if f.endswith(".root")]
    for era_key, era_val in era_map.items():
        with uproot.recreate(f"PileupHistogram-{era_key}-99bins_withVar.root") as fout:
            for key, outname in file_map.items():
                matched = [f for f in root_files if key in f and era_val in f]
                if not matched:
                    print(f"Warning: No file found for {era_val} with key {key} in {year}")
                    continue
                inpath = os.path.join(indir, matched[0])
                with uproot.open(inpath) as fin:
                    h = fin["pileup"]
                    fout[outname] = h
            print(f"Written: PileupHistogram-{era_key}-99bins_withVar.root")