load wavelet_p
load wavelet_h
load wavelet_r

HR=power_h.*power_r;
HP=power_h.*power_p;
dire=atan2(HP,HR)*180/pi;

time=time_h;period=period_h;

% levels = [0:1:max(max(dire))]; %[0.0625,0.125,0.25,0.5,1,2,4,8,16] ;
% Yticks = 2.^(fix(log2(min(period))):fix(log2(max(period))));
% contour(time,log2(period),log2(dire),log2(levels));  %*** or use 'contourfill'
% %imagesc(time,log2(period),log2(power));  %*** uncomment for 'image' plot
% xlabel('Time (seconds)')
% ylabel('Period (seconds)')
% title('b) Wavelet Power Spectrum H=10cm T=0.6s WS8')
% set(gca,'XLim',xlim(:))
% set(gca,'YLim',log2([min(period),max(period)]), ...
% 	'YDir','reverse', ...
% 	'YTick',log2(Yticks(:)), ...
% 	'YTickLabel',Yticks)
% % 95% significance contour, levels at -99 (fake) and 1 (95% signif)
% hold on
% contour(time,log2(period),sig95,[-99,1],'k');
% hold on
% % cone-of-influence, anything "below" is dubious
% plot(time,log2(coi),'k')
% hold off
