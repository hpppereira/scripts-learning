% SORTP

% routine to sort the peaks from the lower to the higher energy


%  IN: fpn, C11

% OUT: op1(spectral peak value)



x=length(fpn);
    for i=1:x,
posfp(i)=find(f==fpn(i));
%op(i)=s(posfp(i));
op(i)=C11(posfp(i));
    end
clear i posfp
         for j=1:100,
k=0;
     for i=1:x-1,
X=op(i)-op(i+1);
  if X>0,
opaux=op(i);
op(i)=op(i+1);
op(i+1)=opaux;
k=1;
  else;end;          % loop if X
     end                % loop for i=...
if k==0,
break;
end                % loop if k
         end                % loop for j=...

op1=op;

clear X opaux i k j

