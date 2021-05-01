    %   
    clc  
    clear  
    close all  
    %%   
    ts = 0.001;  
    fs = 1/ts;  
    t = 0:ts:1000*ts;  
    f = 50;  
    dis = sin(2*pi*f*t); %   
    vel = 2*pi*f.*cos(2*pi*f*t); %   
    acc = -(2*pi*f).^2.*sin(2*pi*f*t); %   
    %   
    % f1 = 400;  
    % dis1 = sin(2*pi*f1*t); %   
    % vel1 = 2*pi*f1.*cos(2*pi*f1*t); %   
    % acc1 = -(2*pi*f1).^2.*sin(2*pi*f1*t); %   
    % dis = dis + dis1;  
    % vel = vel + vel1;  
    % acc = acc + acc1;  
    % ??  
    %   
    acc = acc + (2*pi*f).^2*0.2*randn(size(acc));  
    % ?  
    figure  
    ax(1) = subplot(311);  
    plot(t, dis), title('')  
    ax(2) = subplot(312);  
    plot(t, vel), title('')  
    ax(3) = subplot(313);  
    plot(t, acc), title('')  
    linkaxes(ax, 'x');  
    %   
    [disint, velint] = IntFcn(acc, t, ts, 2);  
    axes(ax(2));   hold on  
    plot(t, velint, 'r'), legend({'', ''})  
    axes(ax(1));   hold on  
    plot(t, disint, 'r'), legend({'', ''})  
    %%   
    n = 30;  
    amp = zeros(n, 1);  
    f = [5:30 40:10:480];  
    figure  
    for i = 1:length(f)  
        fi = f(i);  
        acc = -(2*pi*fi).^2.*sin(2*pi*fi*t); %   
        [disint, velint] = IntFcn(acc, t, ts, 2); %   
        amp(i) = sqrt(sum(disint.^2))/sqrt(sum(dis.^2));  
        plot(t, disint)  
        drawnow  
    %     pause  
    end  
    close  
    figure  
    plot(f, amp)  
    title('')  
    xlabel('f')  
    ylabel('')  