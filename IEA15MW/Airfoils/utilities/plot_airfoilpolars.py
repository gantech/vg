import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import glob, pathlib
from airfoil import *
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

def plot_airfoil_polar(afp_yaml1, filename, afp_yaml2=None, afp_yaml3=None):

    afp = AirfoilTableDB(afp_yaml1)
    afnames = sorted(list(afp.get_airfoils()))

    if (afp_yaml2 is not None):
        afp2 = AirfoilTableDB(afp_yaml2)

    if (afp_yaml3 is not None):
        afp3 = AirfoilTableDB(afp_yaml3)

    plt.style.use('subplot13')
    with PdfPages(filename) as pfpgs:
        for af in afnames:
            fig,axs = plt.subplots(1,3)
            af_data = afp.get_airfoil_data(af)
            axs[0].plot(af_data['aoa'], af_data['cl'],label=r'Nalu-wind')
            stall_angle = afp.lift_stall_angle(af)
            axs[0].plot(stall_angle, afp.get_aftable(af)(stall_angle,'cl'), '+', color='r')
            axs[1].semilogy(af_data['aoa'], af_data['cd'],label=r'Nalu-wind')
            #axs[1,0].plot(af_data['aoa'], af_data['cm'])
            axs[2].plot(af_data['aoa'], af_data['cl']/af_data['cd'], label=r'Nalu-wind')
            aoa_range = [af_data['aoa'].iloc[0], af_data['aoa'].iloc[-1]]
            
            if (afp_yaml2 is not None):
                af_data = afp2.get_airfoil_data(af)
                axs[0].plot(af_data['aoa'], af_data['cl'],label=r'Nalu-wind VG')
                stall_angle = afp.lift_stall_angle(af)
                axs[0].plot(stall_angle, afp.get_aftable(af)(stall_angle,'cl'), '+', color='r')
                axs[1].semilogy(af_data['aoa'], af_data['cd'],label=r'Nalu-wind VG')
                #axs[1,0].plot(af_data['aoa'], af_data['cm'])
                axs[2].plot(af_data['aoa'], af_data['cl']/af_data['cd'],label=r'Nalu-wind VG')
                axs[1].legend(loc=0)

            if (afp_yaml3 is not None):
                af_data = afp3.get_airfoil_data(af)                
                aoa_filter = (af_data['aoa'] >= aoa_range[0]) & (af_data['aoa'] <= aoa_range[1])
                axs[0].plot(af_data['aoa'][aoa_filter], af_data['cl'][aoa_filter],label='IEA15MW')
                stall_angle = afp.lift_stall_angle(af)
                axs[0].plot(stall_angle, afp.get_aftable(af)(stall_angle,'cl'), '+', color='r')
                axs[1].semilogy(af_data['aoa'][aoa_filter], af_data['cd'][aoa_filter],label='IEA15MW')
                #axs[1,0].plot(af_data['aoa'][aoa_filter], af_data['cm'][aoa_filter])
                axs[2].plot(af_data['aoa'][aoa_filter], af_data['cl'][aoa_filter]/af_data['cd'][aoa_filter],label='IEA15MW')
                axs[1].legend(loc=0)

            axs[0].set_xlabel(r'$\alpha$')
            axs[1].set_xlabel(r'$\alpha$')
            axs[2].set_xlabel(r'$\alpha$')
            axs[0].set_ylabel(r'$C_l$')
            axs[1].set_ylabel(r'$C_d$')
            axs[2].set_ylabel(r'$C_l/C_d$')
            axs[0].grid()
            axs[1].grid()
            axs[2].grid()
            plt.tight_layout()
            pfpgs.savefig()
            plt.close(fig)
            
def plot_re_airfoil_polars(rey=[5e6,10e6,15e6]):

    airfoils = [ af.split('/')[-1] for af in glob.glob('nalu_inputs/grids/coordinates/*') ]

    plt.style.use('subplot13')
    with PdfPages('re_airfoil_polars.pdf') as pfpgs:
        for af in airfoils:
            xy = np.loadtxt('nalu_inputs/grids/coordinates/{}'.format(af))
            afcst = AirfoilShape(xy[:,0], xy[:,1])
            tbyc = afcst.get_tbycmax()
            if(tbyc > 0.1):
                fig,axs = plt.subplots(1,3)
                for re in rey:
                    afp = AirfoilTableDB("nalu_results/static/{}_rey{:08d}.yaml".format(af, int(re)))
                    af_data = afp.get_airfoil_data(af)
                    axs[0].plot(af_data['aoa'], af_data['cl'],label=r'Re = {:.1e}'.format(re))
                    stall_angle = afp.lift_stall_angle(af)
                    axs[0].plot(stall_angle, afp.get_aftable(af)(stall_angle,'cl'), '+', color='r')
                    axs[1].semilogy(af_data['aoa'], af_data['cd'],label=r'Re = {:.1e}'.format(re))
                    axs[2].plot(af_data['aoa'], af_data['cl']/af_data['cd'], label=r'Re = {:.1e}'.format(re))
                axs[1].set_title('{} - Exawind'.format(af) + ' t/c = {:.1f}%'.format(float(tbyc)*100.0) )
                axs[0].set_xlabel(r'$\alpha$')
                axs[1].set_xlabel(r'$\alpha$')
                axs[2].set_xlabel(r'$\alpha$')
                axs[0].set_ylabel(r'$C_l$')
                axs[1].set_ylabel(r'$C_d$')
                axs[2].set_ylabel(r'$C_l/C_d$')
                axs[1].legend(loc=0)
                axs[0].grid()
                axs[1].grid()
                axs[2].grid()
                plt.tight_layout()
                pfpgs.savefig()
                plt.close(fig)
                    
            else:
                print(af, ' ', tbyc)
            

if __name__=="__main__":
    #plot_re_airfoil_polars()
    #plot_airfoil_polar('nalu_results/static/airfoils_rey05000000.yaml','nalu_results/airfols_rey05000000.pdf', 'nalu_results/static_vg/airfoils_rey05000000.yaml', None)
    plot_airfoil_polar('nalu_results/static/airfoils_rey10000000.yaml','nalu_results/airfols_rey10000000.pdf', 'nalu_results/static_vg/airfoils_rey10000000.yaml', None)
    #plot_airfoil_polar('nalu_results/static/airfoils_rey15000000.yaml','nalu_results/airfols_rey15000000.pdf', 'nalu_results/static_vg/airfoils_rey15000000.yaml', None)
