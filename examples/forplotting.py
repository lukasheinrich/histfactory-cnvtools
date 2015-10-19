#!/usr/bin/env python

import click
import ROOT
import histfactorycnv as hfc
import random
@click.command()
@click.argument('rootfile')
@click.argument('channel')
@click.argument('components')
@click.option('-w','--workspace', default = 'combined')
@click.option('-o','--outputfile', default = 'plot.png')
@click.option('-v','--observable', default = 'x')
def stackplot(rootfile,channel,components,workspace,outputfile,observable):
  f = ROOT.TFile.Open(rootfile)
  ws = f.Get(workspace)
  components = components.split(',')

  colors = [ROOT.kViolet-1,ROOT.kAzure-9,ROOT.kRed+1,ROOT.kGreen+3]
  stack = ROOT.THStack()
  all_noms = []
  
  
  syst_bands = []
  for sample in reversed(components):
    nom = hfc.extract(ws,channel,observable,sample)

    nom.SetFillColor(ROOT.TColor.GetColor(random.random(),random.random(),random.random()))
    nom.SetLineColor(ROOT.kBlack)
    stack.Add(nom)
    all_noms += [nom]

  
  c = ROOT.TCanvas()

  stack.Draw()

  frame = stack.GetHistogram()

  datahist = hfc.extract_data(ws,channel,observable)
  datahist.SetMarkerStyle(20)
  datahist.SetLineColor(ROOT.kBlack)
  datahist.SetMarkerColor(ROOT.kBlack)
  datahist.Draw('E0same')
  
  c.SaveAs(outputfile)
  
if __name__ == '__main__':
  stackplot()