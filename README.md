# IEEE1451.0_TEDS_Editor
An editor for IEEE 1451.0 TEDS.

Currently supports definition, loading, saving, editing of:
- Meta-TEDS
- TransducerChannelTEDS

## Install PyQT5
```python -m pip istall pyqt5-tools```

## Compile qt5.ui files to Python files
```
python -m PyQt5.uic.pyuic -x teds-editor.ui -o teds_editor.py
python -m PyQt5.uic.pyuic -x teds-sub-editor.ui -o teds_sub_editor.py

```

## Run with
```python main_teds.py```

## Layout
![Main Window](https://github.com/DIGI2-FEUP/IEEE1451.0_TEDS_Editor/blob/main/img/window.png)

A Meta-TEDS binary file from this screenshot [here](https://github.com/DIGI2-FEUP/IEEE1451.0_TEDS_Editor/blob/main/meta_teds_2022-07-03_00-12-17.bin).

![TrasnducerChannelTEDS View](https://github.com/DIGI2-FEUP/IEEE1451.0_TEDS_Editor/blob/main/img/transducer-chann-teds-view.png)

A TrasnducerChannelTEDS file from this screenshot [here](https://github.com/DIGI2-FEUP/IEEE1451.0_TEDS_Editor/blob/main/channel_teds_2022-07-03_00-13-59.bin).

![Nested TEDS sub-block View](https://github.com/DIGI2-FEUP/IEEE1451.0_TEDS_Editor/blob/main/img/aux-window.png)

***Used Python Python 3.5.3rc1 to build this project***
