% ?  
function [disint, velint] = IntFcn(acc, t, ts, flag)  
if flag == 1  
    %   
    [disint, velint] = IntFcn_Time(t, acc);  
    velenergy = sqrt(sum(velint.^2));  
    velint = detrend(velint);  
    velreenergy = sqrt(sum(velint.^2));  
    velint = velint/velreenergy*velenergy;    
    disenergy = sqrt(sum(disint.^2));  
    disint = detrend(disint);  
    disreenergy = sqrt(sum(disint.^2));  
    disint = disint/disreenergy*disenergy; %   
    %   
    p = polyfit(t, disint, 2);  
    disint = disint - polyval(p, t);  
else  
    %   
    velint =  iomega(acc, ts, 3, 2);  
    velint = detrend(velint);  
    disint =  iomega(acc, ts, 3, 1);  
    %   
    p = polyfit(t, disint, 2);  
    disint = disint - polyval(p, t);  
end  
end  