# Copyright (C) 2023 Łebi

import os
import fnmatch
from pathlib import Path, PurePath
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow
from osgeo import gdal

import functions
import bw_pix
import overview
import seamlines
from droparea import DropAreaDir, DropAreaFile

basedir = os.path.dirname(__file__)
gdal.UseExceptions()


class ToolsStudio(QMainWindow):
    def __init__(self):
        super(ToolsStudio, self).__init__()
        self.setWindowIcon(QIcon(os.path.join(basedir, "icons", "python_icon.png")))
        self.setWindowTitle("Tools Studio")
        self.resize(500, 700)
        loader = QUiLoader()
        self.window = loader.load("tools_studio.ui", self)
        #   *****   BW pix   *****
        self.window.lineEdit_bw_path_input = DropAreaDir()
        self.window.lineEdit_bw_path_output = DropAreaDir()
        self.window.gridLayout_bw_path_input.addWidget(self.window.lineEdit_bw_path_input, 1, 0)
        self.window.gridLayout_bw_path_output.addWidget(self.window.lineEdit_bw_path_output, 1, 0)
        self.window.pushButton_bw_path_input.clicked.connect(self.get_bw_path_input)
        self.window.pushButton_bw_path_output.clicked.connect(self.get_bw_path_output)
        self.window.pushButton_bw_start.clicked.connect(self.bw_start)
        #   *****   OverView   *****
        self.window.lineEdit_ov_path_input = DropAreaDir()
        self.window.lineEdit_ov_path_output = DropAreaDir()
        self.window.gridLayout_ov_path_input.addWidget(self.window.lineEdit_ov_path_input, 1, 0)
        self.window.gridLayout_ov_path_output.addWidget(self.window.lineEdit_ov_path_output, 1, 0)
        self.window.lineEdit_ov_path_output.setEnabled(False)
        self.window.pushButton_ov_path_output.setEnabled(False)
        self.window.frame_ov_selected.setEnabled(False)
        self.window.frame_ov_tile.setEnabled(False)
        self.window.frame_ov_compress.setEnabled(False)
        self.window.pushButton_ov_clean.setEnabled(False)
        self.window.checkBox_ov_clean_tile.setEnabled(False)
        self.window.pushButton_ov_path_input.clicked.connect(self.get_ov_path_input)
        self.window.pushButton_ov_path_output.clicked.connect(self.get_ov_path_output)
        self.window.checkBox_ov_path_output.stateChanged.connect(self.open_ov_path_output)
        self.window.radioButton_ov_none.toggled.connect(self.close_ov_compress_yes)
        self.window.radioButton_ov_selected.toggled.connect(self.open_ov_frame)
        self.window.checkBox_ov_tile.stateChanged.connect(self.open_ov_frame_tile)
        self.window.checkBox_ov_compress.stateChanged.connect(self.open_ov_frame_compress)
        self.window.checkBox_ov_clean_ov.stateChanged.connect(self.open_ov_clean,)
        self.window.checkBox_ov_clean_ov.stateChanged.connect(self.open_ov_clean_tile)
        self.window.checkBox_ov_clean_geometry.stateChanged.connect(self.open_ov_clean)
        self.window.pushButton_ov_start.clicked.connect(self.ov_start)
        self.window.pushButton_ov_clean.clicked.connect(self.ov_clean)
        #   *****   Linia Mozaikowania   *****
        self.window.lineEdit_moz_path_input = DropAreaFile()
        self.window.lineEdit_moz_path_input.getFileType(file_type=".dxf")
        self.window.lineEdit_moz_path_output = DropAreaDir()
        self.window.gridLayout_moz_path_input.addWidget(self.window.lineEdit_moz_path_input, 1, 0)
        self.window.gridLayout_moz_path_output.addWidget(self.window.lineEdit_moz_path_output, 1, 0)
        self.window.pushButton_moz_path_input.clicked.connect(self.get_moz_path_input)
        self.window.pushButton_moz_path_output.clicked.connect(self.get_moz_path_output)
        self.window.pushButton_moz_start.clicked.connect(self.moz_start)

    #   *****   BW pix   *****
    @Slot()
    def get_bw_path_input(self):
        self.window.lineEdit_bw_path_input.setText(functions.get_path())

    @Slot()
    def get_bw_path_output(self):
        self.window.lineEdit_bw_path_output.setText(functions.get_path())

    @Slot()
    def bw_start(self):
        path_input = self.window.lineEdit_bw_path_input.text()
        path_output = self.window.lineEdit_bw_path_output.text()
        path_type = "input"                                         ## type: input, output
        if functions.check_path(path_input, path_type):
            path_input = Path(path_input)
            path_type = "output"
            if functions.check_path(path_output, path_type):
                path_output = Path(path_output)
                if functions.compare_path(path_input, path_output):
                    nr_of_files = functions.count_files(path_input, "*.tif")
                    if nr_of_files != 0:
                        self.window.progressBar.setMaximum(nr_of_files)
                        count = 0
                        for file in os.listdir(path_input):
                            if fnmatch.fnmatch(file, "*.tif"):
                                try:
                                    count += 1
                                    self.window.progressLabel.setText("  " + str(count) + " / "
                                                                      + str(nr_of_files) + "  -  " + file)
                                    bw_pix.process(path_input, path_output, file)
                                    self.window.progressBar.setValue(count)
                                except:
                                    count -= 1
                                    functions.error(path_input, path_output, file)
                        functions.summary(nr_of_files, count)
                        self.window.progressLabel.setText("")
                        self.window.progressBar.setValue(0)

    #   *****   OverView   *****
    @Slot()
    def get_ov_path_input(self):
        self.window.lineEdit_ov_path_input.setText(functions.get_path())

    @Slot()
    def get_ov_path_output(self):
        self.window.lineEdit_ov_path_output.setText(functions.get_path())

    @Slot()
    def open_ov_path_output(self):
        if self.window.checkBox_ov_path_output.isChecked():
            self.window.lineEdit_ov_path_output.setEnabled(True)
            self.window.pushButton_ov_path_output.setEnabled(True)
        else:
            self.window.lineEdit_ov_path_output.setEnabled(False)
            self.window.lineEdit_ov_path_output.setText("")
            self.window.pushButton_ov_path_output.setEnabled(False)

    @Slot()
    def close_ov_compress_yes(self):
        if self.window.radioButton_ov_none.isChecked():
            self.window.radioButton_ov_compress_ov_no.setChecked(True)
            self.window.radioButton_ov_compress_ov_yes.setEnabled(False)
            self.window.radioButton_ov_compress_ov_no.setEnabled(False)
        else:
            self.window.radioButton_ov_compress_ov_yes.setEnabled(True)
            self.window.radioButton_ov_compress_ov_no.setEnabled(True)

    @Slot()
    def open_ov_frame(self):
        if self.window.radioButton_ov_selected.isChecked():
            self.window.frame_ov_selected.setEnabled(True)
        else:
            self.window.frame_ov_selected.setEnabled(False)
            self.window.checkBox_2.setChecked(False)
            self.window.checkBox_4.setChecked(False)
            self.window.checkBox_8.setChecked(False)
            self.window.checkBox_16.setChecked(False)
            self.window.checkBox_32.setChecked(False)
            self.window.checkBox_64.setChecked(False)
            self.window.checkBox_128.setChecked(False)
            self.window.checkBox_256.setChecked(False)
            self.window.checkBox_512.setChecked(False)
            self.window.checkBox_1024.setChecked(False)

    @Slot()
    def open_ov_frame_tile(self):
        if self.window.checkBox_ov_tile.isChecked():
            self.window.frame_ov_tile.setEnabled(True)
            self.window.radioButton_ov_tile_256.setChecked(True)
        else:
            self.window.frame_ov_tile.setEnabled(False)
            self.window.radioButton_ov_tile_256.setChecked(True)

    @Slot()
    def open_ov_frame_compress(self):
        if self.window.checkBox_ov_compress.isChecked():
            self.window.frame_ov_compress.setEnabled(True)
        else:
            self.window.frame_ov_compress.setEnabled(False)
            self.window.spinBox_ov_compress.setValue(95)

    @Slot()
    def open_ov_clean(self):
        if self.window.checkBox_ov_clean_ov.isChecked() or self.window.checkBox_ov_clean_geometry.isChecked():
            self.window.pushButton_ov_clean.setEnabled(True)
            self.window.pushButton_ov_start.setEnabled(False)
            self.window.checkBox_ov_path_output.setChecked(False)
            self.window.checkBox_ov_path_output.setEnabled(False)
            self.window.lineEdit_ov_path_output.setEnabled(False)
            self.window.lineEdit_ov_path_output.setText("")
            self.window.pushButton_ov_path_output.setEnabled(False)
        else:
            self.window.pushButton_ov_clean.setEnabled(False)
            self.window.pushButton_ov_start.setEnabled(True)
            self.window.checkBox_ov_path_output.setEnabled(True)

    @Slot()
    def open_ov_clean_tile(self):
        if self.window.checkBox_ov_clean_ov.isChecked():
            self.window.checkBox_ov_clean_tile.setEnabled(True)
        else:
            self.window.checkBox_ov_clean_tile.setChecked(False)
            self.window.checkBox_ov_clean_tile.setEnabled(False)

    @Slot()
    def ov_start(self):
        path_input = self.window.lineEdit_ov_path_input.text()
        path_type = "input"                                         ## type: input, output
        if functions.check_path(path_input, path_type):
            path_input = Path(path_input)
            nr_of_files = functions.count_files(path_input, "*.tif")
            if nr_of_files != 0:
                self.window.progressBar.setMaximum(nr_of_files)
                path_output = self.window.lineEdit_ov_path_output.text()
                if self.window.checkBox_ov_path_output.isChecked():
                    path_type = "output"
                    if functions.check_path(path_output, path_type):
                        path_output = Path(path_output)
                        if functions.compare_path(path_input, path_output):
                            self.ov_check(path_input, path_output, nr_of_files)
                else:
                    path_output = ""
                    self.ov_check(path_input, path_output, nr_of_files)

    def ov_check(self, path_input, path_output, nr_of_files):
        resampling = " -r " + str.lower(self.window.comboBox_ov_resampling.currentText())
        if self.window.radioButton_ov_compress_ov_yes.isChecked():
            resampling = (' --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR'
                          ' --config INTERLEAVE_OVERVIEW PIXEL') + resampling
        if self.window.checkBox_ov_tile.isChecked():
            if self.window.radioButton_ov_tile_none.isChecked():
                tile = ' -co "TILED=NO"'
            elif self.window.radioButton_ov_tile_128.isChecked():
                tile = ' -co "TILED=YES" -co "BLOCKXSIZE=128" -co "BLOCKYSIZE=128"'
            elif self.window.radioButton_ov_tile_256.isChecked():
                tile = ' -co "TILED=YES" -co "BLOCKXSIZE=256" -co "BLOCKYSIZE=256"'
            elif self.window.radioButton_ov_tile_512.isChecked():
                tile = ' -co "TILED=YES" -co "BLOCKXSIZE=512" -co "BLOCKYSIZE=512"'
            elif self.window.radioButton_ov_tile_1024.isChecked():
                tile = ' -co "TILED=YES" -co "BLOCKXSIZE=1024" -co "BLOCKYSIZE=1024"'
        else:
            tile = ""
        if self.window.radioButton_ov_none.isChecked():
            ov = ""
            self.ov_check_compress(path_input, path_output, nr_of_files, resampling, ov, tile)
        elif self.window.radioButton_ov_selected.isChecked():
            ov = ""
            box_2 = ""
            box_4 = ""
            box_8 = ""
            box_16 = ""
            box_32 = ""
            box_64 = ""
            box_128 = ""
            box_256 = ""
            box_512 = ""
            box_1024 = ""
            if self.window.checkBox_2.isChecked():
                box_2 = " 2"
            if self.window.checkBox_4.isChecked():
                box_4 = " 4"
            if self.window.checkBox_8.isChecked():
                box_8 = " 8"
            if self.window.checkBox_16.isChecked():
                box_16 = " 16"
            if self.window.checkBox_32.isChecked():
                box_32 = " 32"
            if self.window.checkBox_64.isChecked():
                box_64 = " 64"
            if self.window.checkBox_128.isChecked():
                box_128 = " 128"
            if self.window.checkBox_256.isChecked():
                box_256 = " 256"
            if self.window.checkBox_512.isChecked():
                box_512 = " 512"
            if self.window.checkBox_1024.isChecked():
                box_1024 = " 1024"
            ov = box_2 + box_4 + box_8 + box_16 + box_32 + box_64 + box_128 + box_256 + box_512 + box_1024
            if functions.check_ov(ov):
                self.ov_check_compress(path_input, path_output, nr_of_files, resampling, ov, tile)
        elif self.window.radioButton_ov_full.isChecked():
            ov = " 2 4 8 16 32 64 128 256 512 1024"
            self.ov_check_compress(path_input, path_output, nr_of_files, resampling, ov, tile)

    def ov_check_compress(self, path_input, path_output, nr_of_files, resampling, ov, tile):
        if self.window.checkBox_ov_compress.isChecked():
            q = str(self.window.spinBox_ov_compress.value())
            compress = ' -co "COMPRESS=JPEG" -co "JPEG_QUALITY=' + q + '" -co "PHOTOMETRIC=YCBCR"'
            if self.window.checkBox_ov_path_output.isChecked():
                self.overview(path_input, path_output, nr_of_files, resampling, ov, tile, compress)
            else:
                functions.compress_message()
        else:
            compress = ""
            self.overview(path_input, path_output, nr_of_files, resampling, ov, tile, compress)

    def overview(self, path_input, path_output, nr_of_files, resampling, ov, tile, compress):
        if ov == "" and tile == "" and compress == "":
            functions.overview_message()
        else:
            count = 0
            for file in os.listdir(path_input):
                if fnmatch.fnmatch(file, "*.tif"):
                    try:
                        count += 1
                        self.window.progressLabel.setText("  " + str(count) + " / "
                                                          + str(nr_of_files) + "  -  " + file)
                        ds = gdal.Open(os.path.join(path_input, file))
                        ds = None
                        overview.process(path_input, path_output, resampling, ov, tile, compress, file)
                        self.window.progressBar.setValue(count)
                    except:
                        count -= 1
                        functions.error(path_input, path_output, file)
            functions.summary(nr_of_files, count)
            self.window.progressLabel.setText("")
            self.window.progressBar.setValue(0)

    @Slot()
    def ov_clean(self):
        clean_ov = self.window.checkBox_ov_clean_ov.isChecked()
        clean_tile = self.window.checkBox_ov_clean_tile.isChecked()
        clean_geometry = self.window.checkBox_ov_clean_geometry.isChecked()
        path_input = self.window.lineEdit_ov_path_input.text()
        path_type = "input"                                         ## type: input, output
        if functions.check_path(path_input, path_type):
            path_input = Path(path_input)
            nr_of_files = functions.count_files(path_input, "*.tif")
            if nr_of_files != 0:
                self.window.progressBar.setMaximum(nr_of_files)
                count = 0
                for file in os.listdir(path_input):
                    if fnmatch.fnmatch(file, "*.tif"):
                        try:
                            count += 1
                            self.window.progressLabel.setText("  " + str(count) + " / "
                                                              + str(nr_of_files) + "  -  " + file)
                            overview.clean(path_input, clean_ov, clean_tile, clean_geometry, file)
                            self.window.progressBar.setValue(count)
                        except:
                            count -= 1
                            functions.error(path_input, "", file)
                functions.summary(nr_of_files, count)
                self.window.progressLabel.setText("")
                self.window.progressBar.setValue(0)

    #   *****   Linia Mozaikowania   *****
    @Slot()
    def get_moz_path_input(self):
        self.window.lineEdit_moz_path_input.setText(functions.get_file_dxf())

    @Slot()
    def get_moz_path_output(self):
        self.window.lineEdit_moz_path_output.setText(functions.get_path())

    @Slot()
    def moz_start(self):
        file = self.window.lineEdit_moz_path_input.text()
        path_output = self.window.lineEdit_moz_path_output.text()
        file_type = ".dxf"
        if functions.check_file(file, file_type):
            file = Path(file)
            file_name = PurePath(file).name
            path_type = "output"                                         ## type: input, output
            if functions.check_path(path_output, path_type):
                path_output = Path(path_output)
                self.window.progressBar.setMaximum(1)
                self.window.progressLabel.setText(file_name)
                seamlines.process(file, path_output)
                self.window.progressBar.setValue(1)
                #functions.summary(nr_of_files, count)
                self.window.progressLabel.setText("")
                self.window.progressBar.setValue(0)
