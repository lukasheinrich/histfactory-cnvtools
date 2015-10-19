#!/usr/bin/env python

import click
import ROOT
import histfactorycnv as hfc

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
  click.echo('compontents: {}'.format(components))

  colors = {'signal':ROOT.kAzure-9,'background1':ROOT.kRed+1,'background2':ROOT.kViolet-1}
  stack = ROOT.THStack()
  all_noms = []
  
  syst_bands = []
  for sample in reversed(components):
    nom = hfc.extract(ws,channel,observable,sample)
    nom.SetFillColor(colors[sample])
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