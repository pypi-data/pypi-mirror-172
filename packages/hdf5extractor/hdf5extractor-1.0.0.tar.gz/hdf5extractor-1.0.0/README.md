# hdf5-extractor

# installation :

## With poetry :

```console
poetry add hdf5extractor
```

## With pip :

```console
pip install hdf5extractor
```

# Run :

Extract a small h5 from a bigger one, to only have dataset of a specific resqml file : 
```console
extracth5 -i myResqmlFile.xml --h5 myH5File.h5 -o outputFolder
```

Extract every h5 parts from a bigger one, to only have in each, the dataset of a specific resqml file inside an epc : 
```console
extracth5 -i myEPCFile.epc --h5 myH5File.h5 -o outputFolder
```