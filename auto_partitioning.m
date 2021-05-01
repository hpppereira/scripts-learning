clear all; close all; clc;

for j = 31;
    for ii = 1:3:7;
        delete('fort.10','fort.20','fort.21','fort.22','fort.23','fort.24','fort.26',...
            'fort.27','fort.28','fort.32','fort.42','fort.43','fort.44','fort.45','fort.46',...
            'fort.47','fort.245','fort.321')
        if j<10 & ii<10
            eval(['load spec2425_92030',num2str(j),'0',num2str(ii,'%2.0i'),'.mat']);
            eval(['spec = spec_b2030',num2str(j),'0',num2str(ii)]);
            eval(['date = 92030',num2str(j),'0',num2str(ii)]);
        else if j<10 & ii>=10
                eval(['load spec2425_92030',num2str(j),num2str(ii,'%2.0i'),'.mat']);
                eval(['spec = spec_b2030',num2str(j),num2str(ii)]);
                eval(['date = 92030',num2str(j),num2str(ii)]);
            else if j>=10 & ii<10
                    eval(['load spec2425_9203',num2str(j),'0',num2str(ii,'%2.0i'),'.mat']);
                    eval(['spec = spec_b203',num2str(j),'0',num2str(ii)]);
                    eval(['date = 9203',num2str(j),'0',num2str(ii)]);
                else if j>=10 & ii>=10
                        eval(['load spec2425_9203',num2str(j),num2str(ii,'%2.0i'),'.mat']);
                        eval(['spec = spec_b203',num2str(j),num2str(ii)]);
                        eval(['date = 9203',num2str(j),num2str(ii)]);
                    end
                end
            end
        end
        
        datestr = num2str(date);
        %% Parâmetros para Particionamento e identificação
        %         Parametros
        
        %% Particionamento (Adaptações-Nelson)
        disp('Fazendo particionamento')
        monta_f10
        
        !./partinvbuoy.x
        !ifort readfort20new.f -o readfort20new.x
        !./readfort20new.x
        
        readfort245new
        
        %% Salvando as variáveis geradas
        if j<10 & ii<10
            eval(['save partic_boia_mar92030',num2str(j),'0',num2str(ii),'.mat'])
            delete('readfort20new.x')
            eval(['clear partic_boia_mar_92030',num2str(j),'0',num2str(ii) ])
            eval(['clear spec2425_b2030',num2str(j),'0',num2str(ii) ])
        else if j<10 & ii>=10
                eval(['save partic_boia_mar92030',num2str(j),num2str(ii),'.mat'])
                delete('readfort20new.x')
                eval(['clear partic_boia_mar_92030',num2str(j),num2str(ii) ])
                eval(['clear spec2425_b2030',num2str(j),num2str(ii) ])
            else if j>=10 & ii<10
                    eval(['save partic_boia_mar9203',num2str(j),'0',num2str(ii),'.mat'])
                    delete('readfort20new.x')
                    eval(['clear partic_boia_mar_9203',num2str(j),'0',num2str(ii) ])
                    eval(['clear spec2425_b203',num2str(j),'0',num2str(ii) ])
                    
                else if j>=10 & ii>=10
                        eval(['save partic_boia_mar9203',num2str(j),num2str(ii),'.mat'])
                        delete('readfort20new.x')
                        eval(['clear partic_boia_mar_9203',num2str(j),num2str(ii) ])
                        eval(['clear spec2425_b203',num2str(j),num2str(ii) ])
                    end
                end
            end
        end
        
        %% Plotando o espectro após particionamento e as partições
                frequencia_25 = [0.0412,0.0453,0.0498,0.0548,0.0603,0.0663,0.0730,0.0802,0.0883,0.0971,0.1070,0.1170,0.1290,...
                0.1420,0.1560,0.1720,0.1890,0.2080,0.2290,0.2520,0.2770,0.3050,0.3350,0.3690,0.4060]';
                theta = [0:15:360]';
                theta_Azspecrad = (theta.*pi)./180;
        
%         load frequencia_25.mat
%         load theta_Azspecrad.mat
%         theta_Az_rad = [8.5024;theta_Az_rad];
        
        
        [df,ddir] = meshgrid(frequencia_25,theta_Azspecrad);
        
        for kk = 0:npart-1;
            
             eval(['spec2525 = [specfg_part_',num2str(kk),'(1:24,:);specfg_part_',num2str(kk),'(1,:)];'])
%             eval(['spec2525 = specfg_part_',num2str(kk),';'])
            figure
            h = polar([theta_Azspecrad(1) theta_Azspecrad(end)], [0 0.5]);hold on;
            set(gca,'View',[-90 90],'YDir','reverse');
            %             set(gca,'View',[90 -90]);
            delete(h);
            [px,py]=pol2cart(ddir,df);
            m=max(max(spec2525));
            v=logspace(log10(m/10), log10(m), 150);
            contourf(px,py,real(spec2525),v,'linestyle','none');
            caxis([0,ceil(max(max(spec2525)))])
            colorbar('clim',[0,ceil(max(max(spec2525)))],'YTick',[0:ceil(max(max(spec2525)))])
            get(findall(gcf, 'type', 'text'), 'string');
            thext = {'0' '1' '2' '3' '4' '30' '60' '90' '120' '150' '180' '210' '240' '270' '300' '330' '360'};
            for r=1:length(thext)
                delete(findall(gcf, 'string', thext{r}))
            end
            titulo = ['ESPECTRO DIRECIONAL | Particao-',num2str(kk)]
            title(titulo)
            
            disp('Salvando espectro das partições para cada ponto/hora')
            
            if j<10 & ii<10
                filename = ['espectro_92030',num2str(j),'0',num2str(ii),'_2Dmem_part',num2str(kk)]
            else if j<10 & ii>=10
                    filename = ['espectro_92030',num2str(j),num2str(ii),'_2Dmem_part',num2str(kk)]
                else if j>=10 & ii<10
                        filename = ['espectro_9203',num2str(j),'0',num2str(ii),'_2Dmem_part',num2str(kk)]
                    else if j>=10 & ii>=10
                            filename = ['espectro_9203',num2str(j),num2str(ii),'_2Dmem_part',num2str(kk)]
                        end
                    end
                end
            end
            print ('-depsc','-r150',filename);
            
            clear spec2525
            close all
        end
        
        clearvars -except ii j
        
        
    end
end
