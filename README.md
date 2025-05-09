
# *<center>Visible-Thermal Tiny Object Detection: A Benchmark Dataset and Baselines</center>*

***RGBT-Tiny is a large-scale visible-thermal benchmark, which consists of 115 high-quality paired image sequences, 93K frames and 1.2M manual annotations, and covers abundant targets and diverse scenarios. Details of this dataset can be found in our paper. Over 81\% of targets are smaller than 16x16, and we provide paired bounding box annotations with tracking ID to offer an extremely challenging benchmark with wide-range applications, such as RGBT fusion, detection, and tracking.***<br><be>

**★ Baseline Models and codes will be released in June or July 2025.**<br><br>

## Sample Videos

<center class="half">
     <img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/DJI_0028_5_00_gif.gif" width="500"/>&nbsp&nbsp&nbsp<img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/DJI_0028_5_01_gif.gif" width="500"/>
 </center>

 <center class="half">
     <img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/DJI_0075_3_00_gif.gif" width="500"/>&nbsp&nbsp&nbsp<img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/DJI_0075_3_01_gif.gif" width="500"/>
 </center>

 <center class="half">
     <img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/DJI_0101_2_00_gif.gif" width="500"/>&nbsp&nbsp&nbsp<img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/DJI_0101_2_01_gif.gif" width="500"/>
 </center>

 <center class="half">
     <img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/DJI_0229_2_00_gif.gif" width="500"/>&nbsp&nbsp&nbsp<img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/DJI_0229_2_01_gif.gif" width="500"/>
 </center><br><br>

## Benchmark Properties

### Rich Diversity
<center><img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/target_scene.jpg" width="600"/></center>
Fig. 1 (a) Target distribution in visible and thermal modalities. (b) Scene distribution (inner circle) across different light visions (outer circle). <br> 

### Large Density Variation
<center><img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/density.jpg" width="400"/></center>
Fig. 2 Density of each sequence. (x,y,z) are the numbers of sequences w.r.t. density levels (i.e., sparse, medium, dense).<br> 

### Small-Scale Targets
<center><img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/scale.jpg" width="300"/></center>
Fig. 3 Size distribution of each target category.<br> 

### Temporal Occlusion
<center><img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/occlusion.jpg" width="230"/></center>
Fig. 4 Temporal occlusion (i.e., no occlusion, slight occlusion, moderate occlusion, heavy occlusion).<br> <br> 

## Evaluation Metric
<center><img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/evaluation.jpg" width="1024"/></center>
Fig. 5 An illustration of SAFit measure. (a) Pixels deviation between the center points of GT bbox and predicted bbox. (b) IoU-Deviation curves w.r.t different sizes of bboxes. (c)-(d) SAFit-Deviation curves under different C values. <br>

### SAFit for evaluation
<center><img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/dis_iou.jpg" width="1024"/></center>
Fig. 6 Comparisons among different measures for performance evaluation in visible and thermal modalities.<br>

### SAFit loss for training
SAFit results achieved by ATSS equipped with different losses in visible and thermal modalities of RGBT-Tiny dataset. 
<center><img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/table00.JPG" width="1024"/></center><br>

SAFit and IoU results achieved by ATSS equipped with different losses in COCO dataset.
<center><img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/table01.JPG" width="1024"/></center><br><br>

## Baseline Results
Table 1 SAFit-based results of existing visible detection (V-D), visible SOD (V-SOD), thermal SOD (T-SOD), visible-thermal
detection methods (VT-D) methods on RGBT-Tiny dataset. 
<center><img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/table1.JPG" width="1024"/></center><br>

Table 2 IoU-based results of existing visible detection (V-D), visible SOD (V-SOD), thermal SOD (T-SOD), visible-thermal
detection methods (VT-D) methods on RGBT-Tiny dataset. 
<center><img src="https://raw.github.com/XinyiYing/RGBT-Tiny/master/pics/table2.JPG" width="1024"/></center><br><br>

## Downloads
To access RGBT-Tiny dataset, please fill the following form: 
[[Google Forms]](https://forms.gle/EeRooNEYzXXporQt9), 
[[Microsoft Forms]](https://forms.office.com/r/gQMnp0gp5G)

## Citiation
```
@article{RGBT-Tiny,
 title = {Visible-Thermal Tiny Object Detection: A Benchmark Dataset and Baselines},
 author = {Xinyi Ying and Chao Xiao and Ruojing Li and Xu He and Boyang Li and Xu Cao and Zhaoxu Li and Yingqian Wang and Mingyuan Hu and Qingyu Xu and Zaiping Lin and Miao Li and Shilin Zhou and Wei An and Weidong Sheng and Li Liu},
 journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)},
 year = {2025},
}
```

## MOT label
MOT label for RGBT-Tiny is available at [https://github.com/xuqingyu26/HGTMT](https://github.com/xuqingyu26/HGTMT)

## Contact
Please contact us at ***yingxinyi18@nudt.edu.cn*** for any questions.
