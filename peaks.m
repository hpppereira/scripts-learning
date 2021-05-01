% PEAKS

% routine to select and count the number of peaks of the power spectrum

%  IN: C11 f np=length(C11)

% OUT: fpn freq of the peaks
%      n number of peaks


for i=1:(np-1),
%    dif1(i)=sign(s(i+1)-s(i));
    dif1(i)=sign(C11(i+1)-C11(i));
end

np=length(dif1);

n=0;b=0;a=0;
 for i=1:(np-1),
    dif2(i)=dif1(i+1)-dif1(i);
    if dif2(i)<=-2
          n=n+1;
          fpn(n)=f(i+1);
                   if fpn(n)<=.04; % only below 25s (.04hz)
                   b=b+1;
                   end
                   if fpn(n)>=.26; % only above 3.85s (.26Hz)
                   a=a+1;
                   end
    end
 end


fpn=fpn(b+1:n-a); % freq of the peaks

n=n-b-a; % number of peaks
clear b a i dif1

