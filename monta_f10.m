%    this batch program generates the 2d spec 
%    the output format of Sft_buoy is the same as fort.10, the input for the inversion
%
%   
%     then cp Sft_buoy as fort.10

% load spec2425_p1_19920502_010000
% spec = spec2425_p1_19920502_010000;

fid = fopen('/home/adrieni/Documentos/reananalise_dos_dados11-02/dado_boia/marco_92/espectros_nelson_10-06/adrieni/fort.10','w') % tammy, you have to change here

%  i'm giving dummy values coz it's not important for the processing at the moment, all these values will be calculated by partout2.f
%
       XLON=-29.;
       XLAT=-42.1;
       IDTPRO=strcat(datestr);     
%       IDTPRO=strcat('9',int2str(mountlist(bcont)),'00');     
       XANG=24.;
       XFRE=25.;
       TH0=360.;
       FR=0.0418; 
       CO=1.1;
       HS=1.234;
       THQ=123.;
       FMEAN=0.1234;
       USNEW=1.5;  
       THWNEW=3.14;  

     fwrite(fid,[XLON XLAT str2double(IDTPRO)],'double');
%     fwrite(fid,[XANG XFRE],'float');
%     fwrite(fid,[TH0 FR CO],'double');
     fwrite(fid,HS,'double');
     fwrite(fid,THQ,'double');
     fwrite(fid,FMEAN,'double');
     fwrite(fid,USNEW,'double');
     fwrite(fid,THWNEW,'double');
     fwrite(fid,spec,'double');
fclose all;


clear XLON XLAT IDTRP XANG XFRE TH0 FR C0 HS THQ FMEAN USNEW THWNEW;