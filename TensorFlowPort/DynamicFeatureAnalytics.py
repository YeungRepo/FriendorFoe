#! /usr/env/bin python 

#import matplotlib.pyplot as plt;
#import seaborn as sns;
#from PIL import Image
import cv2;
#from matplotlib.pyplot import imshow
#import matplotlib.patches as patches;
import pickle;
import numpy as np;
#import glob
import os
import time;
import cProfile
pr = cProfile.Profile()
pr.enable()

Start_Time = time.perf_counter()
show_kernels=False;
invert_image = False;
set_kernel=True;
plot_centroids=False;
calibrate_kernels = False;
### Helper Functions ###

def rgb2gray(rgb):
    
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

### Load Kernels ###

#im = Image.open("../Data/Kernels/C2_03_1_1_Bright Field_004.tif");
#im =  cv2.imread("../Data/Kernels/C2_03_1_1_Bright Field_004.tif",-1);
im =  cv2.imread("../Data/Kernels/Healthy_Cell_Repr30x.tif",-1);
#print(np.asarray(im))
#print(im_cv)
#imshow(np.asarray(im))
im_array_gray = im
#im_array_gray = rgb2gray(im_array);
if invert_image:
    im_array_gray = (np.abs(255.0-im_array_gray))

im_array_gray_A549 = im_array_gray;


# Images of Bacterial Patch 

#im = Image.open("../Data/Kernels/runawaygrowth_kernels/P1_E3_09.tif"); # images of bacterial patch
#im = cv2.imread("../Data/Kernels/runawaygrowth_kernels/P1_E3_09.tif",-1); # images of bacterial patch
im = Image.open("Data/Kernels/HCT116-UnhealthyCell_BacterialPatch.tif");
im_array_gray = np.asarray(im,dtype=np.float32)
#im_array_gray = im;# np.asarray(im,dtype=np.float32)
#im_array_gray = rgb2gray(im_array_gray);

if False:
    im_array_gray = (np.abs(255.0-im_array_gray))
im_array_gray_bacterial_patch = im_array_gray#/np.max(im_array_gray);

#imshow(im_array_gray_bacterial_patch)

# Unhealthy cells 

#im = Image.open("../Data/Kernels/Unhealthy_cell_kernels/C6_04_1_1_Bright Field_009.tif");
#im = cv2.imread("../Data/Kernels/Unhealthy_cell_kernels/C6_04_1_1_Bright Field_009.tif",-1);
im = cv2.imread("../Data/Kernels/Unhealthy_cell_kernels/20191113 P1 E1 04.tif"); #Unhealthy_Cell_Repr30x.tif",-1);
#imshow(np.asarray(im))
im_array_gray = np.asarray(im,dtype=np.float32)
#im_array_gray = rgb2gray(im_array_gray);
if False:#invert_image:
     im_array_gray = (np.abs(255.0-im_array_gray))

im_array_gray_A549_UH = im_array_gray

if set_kernel:
    #Define Healthy A549s
    sample_kernel_healthy_A549 = im_array_gray_A549[425:575,1050:1150]
    sample_kernel_healthy_A549 = (np.mean(sample_kernel_healthy_A549,axis=None)-sample_kernel_healthy_A549)/(np.mean(sample_kernel_healthy_A549,axis=None))
    sample_kernel_healthy_A549[sample_kernel_healthy_A549<0.00] =0.0; 
    mask_sample_kernel_healthy_A549 = sample_kernel_healthy_A549;

    #Define Bacterial Patches
    sample_kernel_bacterial_patch = (im_array_gray_bacterial_patch[685:715,685:715]) #np.array(im_array_gray_bacterial_patch[625:795,350:550])#
    sample_kernel_bacterial_patch = (np.mean(sample_kernel_bacterial_patch,axis=None)-sample_kernel_bacterial_patch)/(np.mean(sample_kernel_bacterial_patch,axis=None))
    sample_kernel_bacterial_patch[sample_kernel_bacterial_patch<0.00] =0.0; 
    mask_sample_kernel_bacterial_patch = sample_kernel_bacterial_patch#/np.max(sample_kernel_bacterial_patch);

    
    sample_kernel_unhealthy_A549 = (im_array_gray_A549_UH[540:630,630:730])
    sample_kernel_unhealthy_A549 = (np.mean(sample_kernel_unhealthy_A549,axis=None)-sample_kernel_unhealthy_A549)/(np.mean(sample_kernel_unhealthy_A549,axis=None))
    sample_kernel_unhealthy_A549[sample_kernel_unhealthy_A549<0.00] =0.0;
    sample_kernel_unhealthy_A549[sample_kernel_unhealthy_A549>0.00] =1.0;
    mask_sample_kernel_unhealthy_A549 = sample_kernel_unhealthy_A549;
   
    

if show_kernels ==True:
    import matplotlib.pyplot as plt;
    plt.figure()
    plt.imshow(np.abs(sample_kernel_healthy_A549),cmap='gray')
    plt.title('Healthy A549 Kernel')


    plt.figure()
    plt.imshow(np.abs(sample_kernel_bacterial_patch),cmap='gray')
    plt.title('Bacterial Patch')

    plt.figure()
    plt.imshow(np.abs(sample_kernel_unhealthy_A549),cmap='gray')
    plt.title('Unhealthy A549')

    cbar = plt.colorbar()
    ax = plt.gca()
    ax.set_xticklabels({})
    ax.set_yticklabels({})
    cbar.ax.tick_params(labelsize=20) 

list_of_kernels = [mask_sample_kernel_healthy_A549,mask_sample_kernel_unhealthy_A549,mask_sample_kernel_bacterial_patch]##[mask_sample_kernel_healthy_A549,mask_sample_kernel_healthy_dendritic,mask_sample_kernel_healthy_macrophage,mask_sample_kernel_unhealthy_A549,mask_sample_kernel_unhealthy_dendritic,mask_sample_kernel_unhealthy_macrophage,mask_sample_kernel_bacterial_patch]

list_kernel_families = [None]*len(list_of_kernels);
for sample_kernel_ind in range(0,len(list_of_kernels)):
    mask_sample_kernel = list_of_kernels[sample_kernel_ind];
    base_angle = 0;
    kernel_family = [];
    for delta in range(base_angle,360,10):
        try:
            this_mask_rows,this_mask_cols = mask_sample_kernel.shape;
        except:
            print(sample_kernel_ind)
            print(mask_sample_kernel.shape)
        RotationMat = cv2.getRotationMatrix2D((this_mask_cols/2,this_mask_rows/2),base_angle+delta,1);
        this_family_kernel_img_CV = cv2.warpAffine(mask_sample_kernel,RotationMat,(this_mask_cols,this_mask_rows));
        from PIL import Image
        this_family_kernel_img= Image.fromarray(np.uint8(mask_sample_kernel * 255) ).rotate(angle=base_angle+delta)

        this_family_kernel_img = np.array(this_family_kernel_img,dtype=np.float32)/255.0
        
        kernel_family.append(this_family_kernel_img);
    list_kernel_families[sample_kernel_ind] = kernel_family;

if show_kernels:    
    for kernel_family in list_kernel_families:
        import matplotlib.pyplot as plt;
        figs,list_of_ax = plt.subplots(1,len(kernel_family))
        figs.set_size_inches((30,15))
        for ind in range(0,len(list_of_ax)):
            this_ax = list_of_ax[ind];
            plt.sca(this_ax)
            plt.imshow(kernel_family[ind],cmap='gray')

import itertools

#rootdir = '/Users/eyeung/Box/PNNL\ Friend\ or\ Foe\ Upload/20200318\ A-540\ IV_V\ Pathogens\ T05-T11/20200318\ A-540\ IV_V\ Pathogens\ T05-T11/20200318\ A-540\ IV_V\ Pathogens\ T05-T11/20200318 A-540 IV_V Pathogens T05-T11' ;
#rootdir = '/Users/eyeung/Box/PNNL Friend or Foe Upload/20200318 A-540 IV_V Pathogens T05-T11/20200318 A-540 IV_V Pathogens T05-T11/20200318 A-540 IV_V Pathogens T05-T11';
#rootdir = '/Users/eyeung/Box/PNNL Friend or Foe Upload/20200611 A-549 P1 IV_V Pathogen NegCon #01-02/20200611 A-549 P1 IV_V Pathogen NegCon #01-02';
#rootdir = '/Users/eyeung/Box/PNNL Friend or Foe Upload/20200611 A-549 P1 IV_V Pathogen NegCon #01-02/20200611 A-549 P1 IV_V Pathogen NegCon #01-02';
import sys;
All_Arguments = sys.argv;
rootdir = sys.argv[1];
rootdir = '/home/yeunglab/'+rootdir;
#rootdir = os.path.abspath(rootdir)
exp_id = '/'+rootdir.split('/')[-1] + rootdir.split('/')[-2]
all_orig_files = os.listdir(rootdir);
#filterdir = '/Users/eyeung/Desktop/HighRes_Trial2/'+ rootdir.split('/')[-1];
filterdir = '/home/yeunglab/FoFOutput/Repr_Images/';#'/Users/eyeung/Box/DARPAFoF UCSB Team Share/Repr_Images/';
Pickle_Path = '/home/yeunglab/FoFOutput/Repr_Pickles/';#'/Users/eyeung/Box/DARPAFoF UCSB Team Share/Repr_Pickles/';
all_files = [];

#has_past_processing=False;
#for file in all_orig_files:
#    print(file);
#    if not os.path.isfile(filterdir+'/'+file):
#        all_files.append(file);
#    else:
#        has_past_processing=True;


#all_plate_rows=['A']; #F5  bacterial patch 
#all_plate_cols = ['7']; #F5 is bacterial patch 
all_plate_rows = ['A','B','C','D','E','F','G','H'];
all_plate_cols = ['1','2','3','4','5','6','7','8','9','10','11','12'];

Pos_Flag = list(itertools.product(all_plate_rows,all_plate_cols))
Pos_Flag = [elem[0]+elem[1] for elem in Pos_Flag]



list_of_alphas = [4.4,64.5,26.5];#[3.75,13.0,5.1,8.5,8.2,11.25,4.06]
list_of_colors = ['g','r','b']
import pickle
row_res_masking = 10;
col_res_masking = 10;

kernel_names = ['hA549','uha549','bp']
invert_image = False
##norms_pos_file_suffix = dict();
feature_dict = dict();



for This_Pos_Flag in Pos_Flag:#This will be an iteration over elements like 'A1', 'A2', ... 
    
    
    file_list_suffixes = [elem for elem in all_orig_files if (This_Pos_Flag == elem.split('_')[0] and 1<np.int(elem.split('_')[-1].strip('.tif'))<25) ]
    #file_list_suffixes = [elem for elem in all_orig_files if '15.png' in elem and This_Pos_Flag == elem.split('_')[1]]
    print('Analyzing the following files that match the Position Flag :' + This_Pos_Flag);
    has_past_processing=False;
    for file in all_orig_files:
        if os.path.isfile(filterdir+'/'+rootdir.split('/')[-1]+file):
            has_past_processing=True;
    feature_dict[This_Pos_Flag] = dict();
    if has_past_processing==True:
        print(" - - - Detecting Past Processing on Current Batch of Image Data, loading Existing Feature Dictionary")
        with open(Pickle_Path + '/'+exp_id+'.pickle','rb') as This_Feature_Dict_Pickle:
            feature_dict = pickle.load(This_Feature_Dict_Pickle);
    
    for file_list_suffix in file_list_suffixes:
        TimeKey = file_list_suffix.strip('.tif').split('_')[-1][1:].strip('.png')
        #print(file_list_suffix)
        print(TimeKey)

        feature_dict[This_Pos_Flag][TimeKey] = dict();
        
        filename_in = rootdir +'/' + file_list_suffix;
        check_output_path = filterdir +'/'+ rootdir.split('/')[-1];
        if not(os.path.isdir(check_output_path) ):
            os.mkdir(check_output_path);
        filename_out = filterdir +'/'+ rootdir.split('/')[-1] + '/'+ file_list_suffix;

        im = cv2.imread(filename_in);
        
        im_array_gray = im;#np.asarray(im,dtype=np.float32)
        
        im_array_gray = rgb2gray(im_array_gray);
        
        im_array_gray = im_array_gray[300:700,300:700]
        num_rows = im_array_gray.shape[0];
        num_cols = im_array_gray.shape[1];
        if invert_image:
           im_array_gray = (np.abs(255.0-im_array_gray))

        if plot_centroids:
            import matplotlib.pyplot as plt;
            this_orig_fig = plt.figure(1)#figsize=(35,23));
            this_orig_ax = this_orig_fig.gca() 
            this_orig_ax.imshow(im_array_gray,cmap='gray')
        
            centroid_fig = plt.figure(2)#figsize=(35,23))
            centroid_fig_ax = centroid_fig.gca();
            centroid_fig_ax.imshow(im_array_gray,cmap='gray')


        all_norms_by_kernels=[None]*len(kernel_names);
        all_rects_by_kernels=[None]*len(kernel_names);
        all_centroid_rects_by_kernels = [None]*len(kernel_names);
        all_thresholded_norms_by_kernels = [None]*len(kernel_names);


        for sample_kernel_ind in [0,1,2]:
            mask_sample_kernel = list_of_kernels[sample_kernel_ind];            
            norm_alpha = list_of_alphas[sample_kernel_ind];
            this_color = list_of_colors[sample_kernel_ind];
            this_kernel_family = list_kernel_families[sample_kernel_ind];
            mask_rows = mask_sample_kernel.shape[0]
            mask_cols = mask_sample_kernel.shape[1];
            all_norms_by_kernels[sample_kernel_ind] = [];
            all_rects_by_kernels[sample_kernel_ind] = [];

            all_thresholded_norms_by_kernels[sample_kernel_ind] = im_array_gray-im_array_gray;
            for row_ind in np.arange(0,num_rows-mask_rows,row_res_masking):
                for col_ind in np.arange(0,num_cols-mask_cols,col_res_masking):                                                                                        
                      Raw_Subimage = np.array(im_array_gray[row_ind:row_ind+mask_rows,col_ind:col_ind+mask_cols]);
                      Raw_Subimage = (np.mean(Raw_Subimage,axis=None)-Raw_Subimage)/(np.mean(Raw_Subimage,axis=None))
                      Raw_Subimage[Raw_Subimage<0.0]=0.0;
                      #Family of Kernel Processing Layer
                      base_angle = 0;
                      rotated_norms = [];
                      for rotated_kernel in this_kernel_family:
                          temp_filtered_image = np.array(Raw_Subimage);
                          temp_filtered_image[rotated_kernel==0.0]=0.0;
                          this_norm = np.linalg.norm(rotated_kernel-temp_filtered_image,'fro');
                          rotated_norms.append(1e4*this_norm/(rotated_kernel.shape[0]*rotated_kernel.shape[1]));
                      all_norms_by_kernels[sample_kernel_ind].append(np.min(rotated_norms));#[this_norm,col_ind,row_ind]);
                      if norm_alpha>np.min(rotated_norms):
                          if plot_centroids:
                              import matplotlib.patches as patches
                              this_rect = patches.Rectangle((col_ind,row_ind),mask_cols,mask_rows,linewidth=3,edgecolor=this_color,facecolor='none',alpha=0.2);
                              all_rects_by_kernels[sample_kernel_ind].append(this_rect);
                          all_thresholded_norms_by_kernels[sample_kernel_ind][np.int(row_ind)][np.int(col_ind)] = np.min(rotated_norms);
        #print(len(all_rects_by_kernels[0]))
        #print(len(all_rects_by_kernels[1]))
        #print(len(all_rects_by_kernels[2]))


        
        for sample_kernel_ind in [0,1,2]:
                all_centroid_rects_by_kernels[sample_kernel_ind] = [];
                #print(" - - - - Beginning max pooling - - - -")
                this_color = list_of_colors[sample_kernel_ind];
                mask_sample_kernel = list_of_kernels[sample_kernel_ind];
                mask_rows = mask_sample_kernel.shape[0];
                mask_cols = mask_sample_kernel.shape[1];
                centroid_mask = np.ones((mask_rows,mask_cols));
                num_rows_mf = all_thresholded_norms_by_kernels[sample_kernel_ind].shape[0];
                num_cols_mf = all_thresholded_norms_by_kernels[sample_kernel_ind].shape[1];
                mask_rows_mf = centroid_mask.shape[0]
                mask_cols_mf = centroid_mask.shape[1];
                Post_Image = all_thresholded_norms_by_kernels[sample_kernel_ind] - all_thresholded_norms_by_kernels[sample_kernel_ind] ;
                row_res_mf = np.int(mask_rows/2);
                col_res_mf = np.int(mask_cols/2);
                num_centroids_detect_this_feature = 0;
                unique_centroids = set();
                for row_ind in np.arange(0,num_rows_mf-mask_rows_mf,row_res_mf):
                    for col_ind in np.arange(0,num_cols_mf-mask_cols_mf,col_res_mf):
                        Raw_Subimage = (all_thresholded_norms_by_kernels[sample_kernel_ind][row_ind:row_ind+mask_rows_mf,col_ind:col_ind+mask_cols_mf]);
                        if np.max(Raw_Subimage)>0.0:
                            Raw_Subimage = -Raw_Subimage;
                            Raw_Subimage[Raw_Subimage==0] = -np.Inf;
                            opt_row,opt_col  = np.unravel_index(Raw_Subimage.argmax(),Raw_Subimage.shape)
                            Post_Image[row_ind+opt_row-5:row_ind+opt_row+5,col_ind+opt_col-5:col_ind+opt_col+5] = -np.max(Raw_Subimage) 

                            predicted_centroid_row = (row_ind+opt_row);
                            predicted_centroid_col = (col_ind+opt_col);
                            if not ((predicted_centroid_row,predicted_centroid_col) in unique_centroids):
                                num_centroids_detect_this_feature = num_centroids_detect_this_feature +1;
                                unique_centroids.add((predicted_centroid_row,predicted_centroid_col));
                                if plot_centroids:
                                     import matplotlib.patches as patches;
                                     this_centroid_rect = patches.Rectangle((predicted_centroid_col,predicted_centroid_row),10,10,linewidth=3,edgecolor=this_color,facecolor='none',alpha=0.8);
                                     all_centroid_rects_by_kernels[sample_kernel_ind].append(this_centroid_rect);

                feature_dict[This_Pos_Flag][TimeKey][kernel_names[sample_kernel_ind]] = num_centroids_detect_this_feature;
        



                                ### Activate to show max pooling process 
                                #plt.figure(figsize=(35,23))
                                #plt.imshow(thresholded_norms,cmap='gray')
                                #plt.figure(figsize=(35,23))
                                #plt.imshow(Post_Image,cmap='gray')

        if calibrate_kernels:
            
            
            kernel_names = ['Healthy A549','Unhealthy A549','Bacterial Patches'];
            for this_sample_kernel_ind in [0,1,2]: 
               plt.figure()
               plt.hist(all_norms_by_kernels[this_sample_kernel_ind],bins=200);

               ax = plt.gca()
       #
               ax.spines['right'].set_visible(False)
               ax.spines['top'].set_visible(False)

               # Only show ticks on the left and bottom spines
               ax.yaxis.set_ticks_position('left')
               ax.xaxis.set_ticks_position('bottom')
               plt.ylabel('Frequency/Count',size=20)
               plt.xlabel('Frobenius Norm of Convolution w/ Pathogenicity Feature ',size=20)
               plt.title(kernel_names[this_sample_kernel_ind] + 'Pathogenicity Feature Histogram')



        if plot_centroids:
            for sample_kernel_ind in [0,1,2]:
                for rect in all_rects_by_kernels[sample_kernel_ind]:
                    this_orig_ax.add_patch(rect)
                this_orig_ax.set_title('Features')
            

                
                for rect in all_centroid_rects_by_kernels[sample_kernel_ind]:
                    centroid_fig_ax.add_patch(rect)
                centroid_fig_ax.set_title('Centroids')
            plt.show()


        if plot_centroids:
            plt.show();
            #plt.close('all');
        
        cv2.destroyAllWindows()
        
        del(im);
        del(im_array_gray);
    output_file = open(Pickle_Path+'/'+exp_id+'.pickle','wb')
    pickle.dump(feature_dict,output_file)
    output_file.close()  
    #del(feature_dict);

output_file = open(Pickle_Path+'/'+exp_id+'.pickle','wb')
pickle.dump(feature_dict,output_file)
output_file.close()           
print("Successfully wrote pickle file with feature dictionary!")

print("Total Process Time: " + str( np.float(time.perf_counter()) -np.float(Start_Time)  ))
pr.disable()
pr.print_stats(sort='time')
