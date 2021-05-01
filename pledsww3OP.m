% This is a program for plotting the PLEDS graphics (Parente 1999) using the results of WavewatchIII (PLEDSWW3: Ricardo&Parente 2009)
% The output are the figures (format .eps) for each point-output of WW3.
% The inputs are: prepPLEDS_XX.txt and wind_deph_pos_XX.txt files, where XX is the number of point-output.
%      in fact these files are organized in two list files (listaPleds.txt and listaWind.txt) with all names of prepPLEDS_XX.txt and wind_deph_pos_XX.txt. 
%
% Ricardo Martins Campos & Carlos Eduardo Parente
% riwave@gmail.com
% +1 202 5531739 
% ----------------------------------------------------------------------------------------
% Laboratorio de Instrumentacao Oceanografica (LIOC) AECO/PENO/COPPE/UFRJ  - Rio de Janeiro - Brazil 
% MotorDePopa Wave Research Group
% NCEP / NOAA - National Weather Service 
% ----------------------------------------------------------------------------------------
% Edited by: 
% ----------------------------------------------------------------------------------------
% Contributions: Izabel Nogueira (LIOC/PENO/COPPE/UFRJ) ...
% ----------------------------------------------------------------------------------------
%**************************************************************************

clc
clear all
close all

nt=169;

fid1=fopen('listaPleds.txt','r');
fid2=fopen('listaWind.txt','r');

% Reading the first file 'arqpleds'
arqpleds=fscanf(fid1,'%s',1); 
% Reading the first file 'arqwind'
arqwind=fscanf(fid2,'%s',1); 


mes=['JAN';'FEV';'MAR';'ABR';'MAI';'JUN';'JUL';'AGO'];
mes=[mes;'SET';'OUT';'NOV';'DEZ'];

contc=1;

while ~isempty(arqpleds) 

	mp=load(arqpleds);
	av=load(arqwind);
  
	adirec=mp(:,[7,10,13,16,19]);
	aespec=mp(:,[6,9,12,15,18])*10; 
	ventoc=av(:,6:7);
	dm=av(:,3);
	dm=[dm(1) dm(25) dm(49) dm(73) dm(97) dm(121) dm(145) dm(169)];
	date=av(:,1:4);

        figure;

        c=[0 22.1 0 250];axis(c);
        v6=hanning(15);v61=hanning(11);

        axis('off'  ) 
        col=[0.7 0.7 0.7];

        % vertical lines;
        y=[20;nt+20+30];
        for i=1:1:19,
          x=[i;i];line(x,y,'color',col,'linewidth',[0.2]);
        end

        % horizontal lines with "tick";
        x=[0.9;19.1];
        for i=20:24:nt+1+20,
          y=[i;i];line(x,y,'color',[0.4 0.4 0.4],'linewidth',[0.4]);
        end

        x=[0.5;19.5];
        line(x,y,'color','k','linewidth',[0.6]);

        % horizontal lines
        x=[1;19];
        for i=20:2:nt+10+40,
           y=[i;i];line(x,y,'color',col);
        end

        % Day of the month
        a=22;
        for i=1:length(dm)
          text(.50,a,num2str(dm(i),'%2.2i'),'fontsize',8);
          text(19.1,a,num2str(dm(i),'%2.2i'),'fontsize',8);
          a=a+24.0;
        end

        % Colors of different frequency bands
        arq2=[[1 0 0];[1 0.55 0];[1  1 0];[127/255 1 212/255];[0 0 1]];

        %plotting directional spectrum every day for each frequency band
        %plots from top to bottom
        bb=[0.5;0.5;0.5;0.5;0.5];
        % directional horizontal axis
        a=310:20:720;a=a';
        a1=find(a>360);a(a1)=a(a1)-360;
        for i=1:18,
          text(i+0.15,18,num2str(a(i)),'fontsize',9.5,'color','r','fontweight','bold');
        end;

        text(4.6,14,'Direction (degrees) from which the waves are coming','fontsize',11,'color','r');
        text(0.15,40,'Day of Month','fontsize',11,'rotation',90);

        x=[1;3.1;3.1;1]+3.8;y=[2;2;10;10];
        patch(x,y,arq2(1,:));
        x=x+2.1;patch(x,y,arq2(2,:));
        x=x+2.1;patch(x,y,arq2(3,:));
        x=x+2.1;patch(x,y,arq2(4,:));
        x=x+2.1;patch(x,y,arq2(5,:));

        k1=[];
        k1=['23.92 to 13.31';...
            '13.31 to 8.33 ';...
            ' 8.33 to 5.85 ';...
            ' 5.85 to 3.26 ';...
            ' 3.26 to 1.43 '];

        k=2.81;

        for i=1:5,k=k+2.1;
          text(k,6.5,k1(i,:),'fontsize',7,'color','k','fontweight','bold');
        end;
        text(6.7,-1,'Frequency Band / Periods (s)','fontsize',11,'color','b');
        text(0.4,11.5,'Vertical Scale (waves)','fontsize',9,'color','k')
        text(0.4,6.6,' Hs at each band:','fontsize',9,'color','k')
        text(0.4,1.3,'5 lines = 1 m ','fontsize',10,'color','k')
        text(0.9,223,['PLEDSWW3 (Campos&Parente 2009) Directional Wave Spectrum - WAVEWATCH III'],...
            'fontsize',11,'color','b','fontweight','bold')

        for t=nt:-1:1,
           for i=1:5,

             s1=adirec(t,i); 
             s2=aespec(t,i);
  
             arq=arq2(i,:);%cor  
   
             s11=s1;s12=s2;
      
             b1=s11/20; % direction
             b2=s12; % spectrum  

             if b1>0, 

                b1=b1+3;
                if b1>18,b1=b1-18;
                end;
                b1=b1+1;  % the "zero" starts at 1
                b1=b1+0.5*(rand(1)-0.5);
                n1=t+9+10;  %shift in the vertical scale
         
                v7=linspace(b1-bb(i),b1+bb(i),length(v6));v7=v7';
         
                x=[v7;flipud(v7)];
                   
                y=[(n1+v6*b2);n1*ones(length(v6),1)];
          
                z1=1;z2=1;
         
                if b2.*b1>0,                          
                   patch(x,y,arq);
                end;
                            
             end;
            end;
         end;

         x=[1;7;7;1];y=[1;1;9;9]+210;
         patch(x,y,[1 1 1]);
         text(1.2,215,[num2str(date(1,1),'%4.4i'),num2str(date(1,2),'%2.2i'),num2str(date(1,3),'%2.2i'),' ',num2str(date(1,4),'%2.2i'),'Z'],'fontsize',9,'color','b','fontweight','bold');
         text(3.7,215,' to ','fontsize',10,'color','b');
         text(4.4,215,[num2str(date(end,1),'%4.4i'),num2str(date(end,2),'%2.2i'),num2str(date(end,3),'%2.2i'),' ',num2str(date(end,4),'%2.2i'),'Z'],'fontsize',9,'color','b','fontweight','bold');

         x=[1;5;5;1]+14;y=[4.9;4.9;9.2;9.2]+210;
         patch(x,y,[1 1 1]);

         text(15.07,217,'GFS Surface Wind / WW3','fontsize',8,'color','b');


	for t=nt:-1:1,
		s1=ventoc(t,1);
		s2=ventoc(t,2);

		s2=s2/20;st=t+19;
		s2=s2+3;
		if s2>18,s2=s2-18;end;
		s2=s2+1;
   
		arq=[1 1 1];

		if s1>=5,arq=[0.78 0.78 0.78];end;
		if s1>=10,arq=[0.6 0.6 0.6];end;
		if s1>=15,arq=[0.4 0.4 0.4];end;
		if s1>=20,arq=[0 0 0];end;
		s3=s1;
		s1=s1;

		x=[s2-0.07;s2+0.07;s2+0.07;s2-0.07];
		y=[st;st;st+s1;st+s1];

		if s3>0,
			patch(x,y,arq);
		end;

	end;

	text(15.9,11.5,'Vertical Scale (wind)','fontsize',9,'color','k')
	text(16.1,6.6,' vertical bars:','fontsize',9,'color','k')
	text(16.1,1.3,'8 lines = 15 m/s','fontsize',10,'color','k')

	ld=['NW';'N ';'NE';'E ';'SE';'S ';'SW';'W ';'SW';'W '];
	k=1.55;
	for i=1:8,
		text(k,21.1,ld(i,:),'fontsize',10,'color','k','fontweight','bold');
		k=k+2.25;
	end;

	% Printing 
	set(gcf,'paperposition',[-0.5 -0.5 9.5 11.5]);
	print('-depsc2',['pledsww3_hs_',sprintf('%03d',contc),'.eps'])

	arqpleds=fscanf(fid1,'%s',1); 
	arqwind=fscanf(fid2,'%s',1); 
	contc=contc+1;

end 
fclose(fid1);fclose(fid2);
clear all
close all
quit

% convert -density 130 pledsww3_hs_010.eps pledsww3_hs_010.png

