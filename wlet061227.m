% wlet.m  Driver for producing WDM directional wave spectra plots
%         from wave staff data
%

% M.Donelan / Bergen 1994.11.26
% adjusted for an arbitrary number of the staffs by Alex Babanin / Miami 17.05.2000
% 
% Once wave series data file is ABBBBBB.CCC like,
% the results are stored in a "lBBBBBB.MAT" file and are to be used by
% 'waveplot.m'

clear all
close all % clear Matlab variables and close all Matlab figures

tic % time counter open (look for "toc" below)

%******************************************************************************************
% parameters within this inset have to be adjusted before running the code

np=8;   % number of the wave staffs
D=.93;	% water depth [m] (not necessary if wavenumbers are not needed (see "wavek" below)
%tt = 25*60*53:25*60*83;	% select segment (only if needed) 
n=256; 	% number of points in the FFT segments
lf=.25;	% low frequency margin [Hz] to be calculated
hf=8;		% high frequency margin [Hz] to be calculated
nv=4;		% number of the voices
av=1; 	% parameter for the time series and frequency averaging ns=ns/av;
rest=20;	% 40 degrees restriction on the array opening (see below) 
cf=0.00023;	% conversion into [m] coefficient for the wave series
ns=25;	% sampling frequency [Hz]
pa=1;   %, sec, pause duration

% Load data array with each wave staff time series as a column 

%fname = input('the filename is ');
fname = 'c311908.oc7';
eval(['load c:\data\matlab\lg\card\',fname]);
fname = fname(1:length(fname)-4);	% fname becomes ABBBBBB (see above)
%fname = fname(1:length(fname));
%fname = [fname(1),'a',fname(2),'e',fname(3:length(fname))];
%ws=[.58467*data(:,3) .57756*data(:,1) .59762*data(:,4)];
%ws=[.58467*data(:,3) .57756*data(:,1) .59762*data(:,4) ...
%      .58998*data(:,6) .57155*data(:,5) .57363*data(:,2) ];
%ws = ws(1:length(ws)-4,:);
for i2 = 1:np,
%    if i2 < 5,
      ws(:,i2) = eval([fname,'(:,i2)']);
%       %else   
%   elseif i2 == 5,
%       ws(:,i2) = eval([fname,'(:,i2+1)']);
%    %else
%    %  ws(:,i2) = eval([fname,'(:,i2+2)']);
% end
end
eval(['clear ',fname]);
fprintf('\nData input complete\n');
%disp('Data input complete')

%
%   a and R are the angle [rad] and position [m] of the wave staffs 
%       from the array centre.  
%   np is number of probes
%

% A = [270 198 126 54 342 0]; % LG external array 
% R = [0.15 0.15 0.15 0.15 0.15 0];
% A = [270 198 126 54 0]; % LG external array 
% R = [0.15 0.15 0.15 0.15 0];
%A = [270 198 54 342 0]; 
%R = [0.15 0.15 0.15 0.15 0];
%A = [270 54 342 0]; 
%R = [0.15 0.15 0.15 0];
A = [0-90:360/(np-3):359-90 0 -173-90 -128-90];    % full LG array 
R = [0.15 0.15 0.15 0.15 0.15 0 sqrt(0.0032) 0.04];
%A = [0-90:360/5:359-90 0];  % outer LG array
%R = [0.15 0.15 0.15 0.15 0.15 0];
%A = [270 342 0]; 
%R = [0.15 0.15 0];
%A = [270 126 54];
%R = [0.15 0.15 0.15];
%A = [126 54 0];
%R = [0.15 0.15 0];
%A = [270 198 342];
%R = [0.15 0.15 0.15];
%A = [0 33:72:105];
%R = [0 0.25 0.25 0.25];
%A = [0 33:72:359];
%R = [0 0.25 0.25 0.25 0.25 0.25];
%A = [90 -90 0];
%R = [0.15 0.15 sqrt(0.3^2 -0.15^2)];
%*****************************************************************************************

if exist('tt') == 1,
	ws = ws(tt,:);
end
dr=pi/180;  A = dr*A;
ws = cf*ws;
M=length(fname);
M1=length(ws(:,1));	% record length
t = M1/ns/60;
fprintf('total record length in minutes is %6.2f \n', t);
clear t

figure(1)
for i2=1:np,
   ws(:,i2)=detrend(ws(:,i2));
   ST(i2) = std(ws(:,i2));
   subplot(np,1,i2);
   plot((1:M1)/ns/60,ws(:,i2));
   
   if i2 == 1,
      title(['time series for ',fname,' record'])
   elseif i2 == np,
      xlabel('t, min')
   end
   ylabel('e, m')
   
   ws(:,i2) = ws(:,i2)/ST(i2);
end

pause(pa)

STm = mean(ST)
ws = ws*STm;
% stop	% transition point to MLM

if av ~= 1,
   ws=binavg(ws,av);	% averaging the wave series "av" times (see "av" above)
end
M1=length(ws(:,1));
ns = ns/av;

figure(2)
x = []; nn = [];
for i2=1:np,
   [q,h] = hist(ws(:,i2),50);
   subplot(1,np,i2);
   bar(h,q);
   if i2 == round(np/2),
      title(['histograms for ',fname,' record'])
   end
   x(:,i2) = h'; nn(:,i2) = q';
   clear h q
end
eval(['save h',fname(2:M),' x nn np']);
clear i2 x nn

pause(pa)
%stop

X = R.*cos(A);
Y = R.*sin(A);

l=0;x=[];y=[];
for j=1:np-1,
	for k=(j+1):np,
   		l=l+1;
   		x(l)=X(k)-X(j);
   		y(l)=Y(k)-Y(j);
	end
end

i=sqrt(-1);
r=abs(x+i*y);
a=atan2(y,x);

l=0;rr=[];N=np*(np-1)/2;
for j=1:N-1,
	for k=(j+1):N,
   		l=l+1;
   		rr(l)=a(j)-a(k);
   		csj(l)=cos(a(j));
   		csk(l)=cos(a(k));
   		snj(l)=sin(a(j));
   		snk(l)=sin(a(k));
   		rk(l)=r(k);
   		rj(l)=r(j);
	end
end

rr=rr*180/pi;
ii=find(rr<0);
rr(ii)=rr(ii)+360;
ii=find(rr>90-rest & rr<90+rest);
jj=find(rr>270-rest & rr<270+rest);
ij=sort([ii jj]);

clear ii jj X Y x y rr a r rest

for i1=1:n:M1-n+1,	% the longest loop
	toc	% time counter (see "tic" above)
	lp=log(lf)/log(2);lp=floor(lp);
  	hp=log(hf)/log(2);hp=ceil(hp);

   for i2=1:np,
		eval(['wx',num2str(i2),'=[];'])
		eval(['B',num2str(i2),'=[];'])
      eval(['AMP',num2str(i2),'=[];'])
   end
   eval('AMP=[];')
	clear i2
	
	for jj=1:np,
     		x=ws(i1:i1+n-1,jj);x=x(:);
     		eval(['[wx',num2str(jj),',f]=wavelet(x,lp,hp,nv,ns);'])
     		eval(['B',num2str(jj),'=angle(wx',num2str(jj),');'])
     		eval(['AMP',num2str(jj),'=abs(wx',num2str(jj),');'])
   end
   
   clear d1
 	for i2=1:np-1,
		eval(['AMP1=AMP1+AMP',num2str(i2+1),';'])
	end
   AMP=AMP1/np;
	for i2=1:np,
      eval(['clear AMP',num2str(i2),' wx',num2str(i2)])
   end
   clear i2
      
  	%wn=wavek(f,D);	% Find wavenumbers (doesn't effect the rest of the code)

   clear x 
   if i1 == 1,  
      fprintf('Frequencies are: \n');f
   end   
	mw=mean((abs(AMP)).^2);mf=find(mw==max(mw));
	t=(i1:i1+n-1)/ns;
   figure(1)
   clf
   plot(t,(AMP(:,mf)).^2)
   xlabel('time, sec')
   ylabel('spectral density, m^2sec')
   title(['PSD at the most energetic frequency ',num2str(round(f(mf)*100)/100),' Hz'])
   pause(pa)
   
	mxmf=max(find(f < ns/2));
	kkm=[];thm=[];kks=[];ths=[];

	%********************************************
	for mf=1:mxmf,
	%********************************************

		l=0;b=[];
		for j=1:np-1,
			for k=(j+1):np,
   			l=l+1;
				eval(['b(:,l)=B',num2str(k),'(:,mf)-B',num2str(j),'(:,mf);'])
			end
		end
		ill=find(b(:) > pi); b(ill)=b(ill)-2*pi;
		ill=find(b(:) < -pi); b(ill)=b(ill)+2*pi;

		l=0;AA=[];
		for j=1:N-1,
			for k=(j+1):N,
   			l=l+1;
				AA(:,l)=rk(l)/rj(l)*b(:,j)./b(:,k);
				bk(:,l)=b(:,k);bj(:,l)=b(:,j);
			end
		end

		th=[];ll=0;
		for l=ij,
   		ll=ll+1;
   		th(:,ll)=atan2((AA(:,l)*csk(l)-csj(l)),(snj(l)-AA(:,l)*snk(l)));
   		kk(:,ll)=(snk(l)*bj(:,l)/rj(l)-snj(l)*bk(:,l)/rk(l)) ./ ...
           		    (csj(l)*snk(l) - csk(l)*snj(l))./cos(th(:,ll));
		end
		th = th+(kk<0)*pi;
		kk = abs(kk);

      % More than 3 staffs
      [qq,ww] = size(kk);
		if np>3,
			thm = [thm meanang(th')'];
			ths = [ths std(th')'];
			kkm = [kkm mean(kk')'];
         kks = [kks std(kk')'];
      else
         if ww > 1,
         	thm = [thm meanang(th')'];
            kkm = [kkm mean(kk')'];
         else
            thm = [thm th];
            kkm = [kkm kk];
         end
      end
      %stop
      clear qq ww
      
   end	% end of 'for mf=1:mxmf' loop (frequency bin loop)
   clear AA b bj bk ill th kk j k l 
   
	i1
	if i1 == 1, 
   	AAp=AMP;
   	ddd=round(thm*180/pi);
      kkmp=kkm;
      if floor(M1/n) == 1,
          f1 = f;
          ii = find(f < ns/2);
          f = f(ii);
%          AAp = AAp/av/4;
          eval(['save l',fname(2:M),' AAp ddd kkmp f np STm'])
         f = f1;
         clear f1
      else
         f1 = f;
          ii = find(f < ns/2);
          f = f(ii);
%           AAp = AAp/av/4;
          eval(['save l',fname(2:M),' AAp ddd kkmp np STm'])
          f = f1;
         clear f1
      end
      if np>3,
         clear kkmp ddd AAp
      end
	else
%         f1 = f;
        eval(['load l',fname(2:M)])
        f1 = f;
  		AAp=[AAp;AMP];
  		kkmp=[kkmp;kkm];
  		ddd=[ddd;round(thm*180/pi)];
        ii = find(f < ns/2);
          f = f(ii);
%           AAp = AAp/av/4;
          eval(['save l',fname(2:M),' AAp ddd kkmp f np STm'])
          f = f1;
         clear f1
      if np>3,  
         clear kkmp ddd AAp
      end
   end
   if np == 3,
      clear AAp ddd kkmp f
  end
end

% clear all