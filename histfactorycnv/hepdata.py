#!/usr/bin/env python 

import ROOT
import math
import hepdatarootcnv
import histfactorycnv as hfc
import yaml

def nominal_with_all_systs(dep_info,**kwargs):
  nominal_key = nom = [k for k in dep_info.keys() if 'nominal' in k][0]
  sysnames = [k.split('_')[1] for k in dep_info.keys() if 'systhist' in k and 'up' in k]
  
  nom_val = dep_info[nominal_key]['value']
  
  errors = []
  for sys in sysnames:
    up_val = dep_info['systhist_{}_up'.format(sys)]['value']
    dn_val = dep_info['systhist_{}_down'.format(sys)]['value']
    errors += [{'asymerror':{'minus':dn_val-nom_val,'plus':up_val-nom_val},'label':sys}]

  
  outdata = {'value':nom_val}
  if errors: outdata.update(errors = errors)
  return outdata

def format_column_for_hepdata(ws,channel,observable,component,systematics):
  loaded_param_sets = {}
  x = ws.var(hfc.obsname(observable,channel))
  for name,defin in systematics.iteritems():
    loaded_param_sets[name] = hfc.getsys_pars(defin['HFname'],defin['HFtype'],
                                              workspace = ws, observable = x,
                                              **(defin.get('additional_args',{})))

  
  firstnom = None
  syst_hists = []
  for name,paramset in loaded_param_sets.iteritems():
    up,nom,down = [hfc.extract_with_pars(ws,channel,observable,component,pardict) for pardict in paramset]

    for h,tag in zip([up,down],['up','down']):
      h.SetName('systhist_{}_{}'.format(name,tag))
    
    if not firstnom:
      firstnom = nom
    
    syst_hists += [up,down]

  if not loaded_param_sets:
    #just take reference parameter set
    firstnom = hfc.extract_with_pars(ws,channel,observable,component,{})

  firstnom.SetName("nominal_{}".format(channel))
  
  nom_systs = {h.GetName():h for h in [firstnom] + syst_hists}
  
  column_data = {
   'header': {'name': component},
   'conversion':{
     'formatter': nominal_with_all_systs,
     'inputs': nom_systs
    },
  }
  
  return column_data
  

def hepdata_table(ws,channel,observable,sampledef):
  compcols = []
  for sample,sampledef in sampledef:
    compcols += [format_column_for_hepdata(ws,channel,observable,sample,sampledef['systs'])]
  
  datacol = {
   'header': {'name': 'Data'},
   'conversion':{
     'formatter': hepdatarootcnv.formatters.standard_format,
     'formatter_args': {},
     'inputs': {'histo': hfc.extract_data(ws,channel,observable)}
    },
  }
  
  allcols = [datacol]+ compcols
  
  to_convert = {
    'name': 'Channel {}'.format(channel),
    'dependent_variables': allcols,
    'independent_variables':
    [
      {'header': {'name': observable}}
    ],
  }
  hepdata_formatted = hepdatarootcnv.convertROOT(to_convert)
  return hepdata_formatted

if __name__=='__main__':
  convert()