#!/usr/bin/env python 
import click
import ROOT
import histfactorycnv.hepdata as hft_hepdata
import yaml
import sys

def main():
  rootfile,workspace,channel,observable,outputfile = sys.argv[1:]
  
  signal_systematics = {
    'overallsys':{
      'HFname':'OverallSyst1',
      'HFtype':'OverallSys',
    },
    'histosys':{
      'HFname':'HistoSys1',
      'HFtype':'HistoSys'
    },
    'shapesys1':{
      'HFname':'ShapeSysOne',
      'HFtype':'ShapeSys',
      'additional_args':{
        'constraint_type':'Gaussian'
      }
    },
    'shapesys2':{
      'HFname':'ShapeSysTwo',
      'HFtype':'ShapeSys',
      'additional_args':{
        'constraint_type':'Poisson'
      }
    },
    'lumi':{
      'HFname':'Lumi',
      'HFtype':'Lumi',
    }
  }
  
  background_systematics = {
    'lumi':{
      'HFname':'Lumi',
      'HFtype':'Lumi',
    }
  }
  
  sample_definition = [
    ('signal',{
      'systs': signal_systematics
    }),
    ('background',{
      'systs': background_systematics
    })
  ]
  
  f  = ROOT.TFile.Open(rootfile)
  ws = f.Get(workspace)
  
  hepdata_table = hft_hepdata.hepdata_table(ws,channel,observable,sample_definition)
  
  with open(outputfile,'w') as f:
    f.write(yaml.safe_dump(hepdata_table,default_flow_style = False))

if __name__=='__main__':
  main()