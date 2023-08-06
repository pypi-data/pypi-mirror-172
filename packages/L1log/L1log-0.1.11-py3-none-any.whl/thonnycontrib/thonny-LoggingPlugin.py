from thonnycontrib.thonny_LoggingPlugin.configuration.globals import URL_TERMS_OF_USE, WB
from thonnycontrib.thonny_LoggingPlugin import mainApp

from thonnycontrib.thonny_LoggingPlugin.configuration import configuration
from thonny.config import *

import tkinter as tk
import webbrowser

from thonny import ui_utils
from thonny.ui_utils import CommonDialog
from thonny.languages import get_button_padding, tr
from typing import Optional

def load_plugin():
    """
    Load the plugin and and a command to configure it in thonny
    """
    configuration.init_options()

    if configuration.get_option("first_run") :
        reponse = display_terms_of_use()
        configuration.accept_terms_of_uses(reponse)
        WB.set_option("loggingPlugin.first_run",False)

    logger = mainApp.EventLogger()
    WB.add_configuration_page("LoggingPlugin", "LoggingPlugin", configuration.plugin_configuration_page, 30)
    
    WB.add_command( command_id="about_logger",
                    menu_name="tools",
                    command_label="Logging Plugin",
                    handler=display_about_plugin)
    return

def display_about_plugin():
    '''
    Affiche une pop-up avec une url.
    '''
    ui_utils.show_dialog(AboutLoggingPlugin(WB))

def display_terms_of_use():
    '''
    Ouvre la fenêtre de consentement. Renvoie True si l'utilisateur
    est d'accord pour la collecte de ses données.
    
    Result:
       (bool) vrai si l'utilisateur a cliqué sur "oui", faux
       pour toute autre interaction.
    '''
    fenetre_consentement = ConsentementDialog(WB)
    ui_utils.show_dialog(fenetre_consentement)
    reponse = fenetre_consentement.get_result()
    return reponse == "oui"

    
class AboutLoggingPlugin(CommonDialog):
    '''
    Définit une pop-up avec une url d'info.
    '''
    def __init__(self, master):
        import webbrowser

        super().__init__(master)

        main_frame = tk.ttk.Frame(self, width = 800, height = 100)
        main_frame.grid(sticky=tk.NSEW, ipadx=50, ipady=100)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        self.title("About Thonny_LoggingPLugin")



        url_font = tk.font.nametofont("TkDefaultFont").copy()
        url_font.configure(underline=1)
        url_label = tk.ttk.Label(
            main_frame, text=URL_TERMS_OF_USE, style="Url.TLabel", cursor="hand2", font=url_font
        )
        url_label.grid()
        url_label.bind("<Button-1>", lambda _: webbrowser.open(URL_TERMS_OF_USE))



# Mirabelle
# inspiré de thonny.ui_utils.QueryDialog, certaines choses sont
# peut-être inutiles.
class ConsentementDialog(ui_utils.CommonDialogEx):
    '''
    Définition d'une pop-up lancée au premier démarrage de Thonny
    qui demande si l'utilisateur consent à ce qu'on collecte 
    ses données.
    Si la fenêtre est fermée sans avoir cliqué oui ou non, 
    l'absence de réponse est interprétée comme "non".
    '''
    def __init__(
            self,
            master,
            entry_width: Optional[int] = None,
    ):
        super().__init__(master)

        # question posée
        self.question="Acceptez vous que les données utilisateur issues de Thonny soient collectées\n à des fins de recherche ?"
        bold_font = tk.font.nametofont("TkDefaultFont").copy()
        bold_font.configure(weight=tk.font.BOLD)
        # autres textes à afficher ds la pop-up            
        self.prompt1="Les commentaires en tête de fichier et le nom du fichier ne sont pas collectés\n car pouvant contenir des données personnelles (nom, prénom, groupe).\n Attention à ne pas faire figurer de données personnelles dans le reste du code."
        self.prompt2="Vous pourrez modifier votre choix à tout moment\n dans le menu outils-->options, onglet LoggingPlugin"
        self.mention_legale_courte1="Les informations recueillies sont enregistrées dans un fichier informatisé par CRIStAL. Ces données font l'objet\nd'un traitement informatique destiné à la collecte automatique des traces numériques laissées par les\napprenant·es dans l’environnement de programmation Thonny et à leur anonymisation. Les destinataires des\ndonnées sont les membres de l'équipe de recherche Noce.\n\nToute personne peut obtenir communication et, le cas échéant, rectification ou suppression des informations\nla concernant, en s'adressant aux responsables du projet (contact-l1log@univ-lille.fr). Pour toute autre question,\nvous avez la possibilité de contacter notre délégué à la protection des données."
        self.dpo="https://www.cristal.univ-lille.fr/contact?categorie=rgpd"
        
        # résultat issu de la pop-up : None, "oui", "non"
        self.result = None

        # ??? 
        margin = self.get_large_padding()
        spacing = margin // 2

        # titre de la pop-up
        self.title("Conditions d'utilisation")

        # positionnement question + annonces
        self.prompt_question = tk.ttk.Label(self.main_frame, text=self.question, font=bold_font)
        self.prompt_question.grid(row=1, column=1, columnspan=2, padx=margin, pady=(margin, spacing))
        self.prompt_label1 = tk.ttk.Label(self.main_frame, text=self.prompt1)
        self.prompt_label1.grid(row=2, column=1, columnspan=2, padx=margin, pady=(margin, spacing))
        self.prompt_label2 = tk.ttk.Label(self.main_frame, text=self.prompt2)
        self.prompt_label2.grid(row=3, column=1, columnspan=2, padx=margin, pady=(margin, spacing))

        # je place le bouton "non" en premier pour qu'il ait le focus
        # par défaut. J'ai essayé focus_set sans aucun effet.
        # Je ne comprends pas...
        # self.non_button.focus_set()

        # bouton non
        self.non_button = tk.ttk.Button(
            self.main_frame, text=tr("non"), command=self.on_non, default="active")
        self.non_button.grid(row=5, column=1, padx=(margin, spacing), pady=(0, margin))

        # bouton oui
        self.oui_button = tk.ttk.Button(
        self.main_frame, text=tr("oui"), command=self.on_oui, default="active")
        self.oui_button.grid(row=4, column=1, padx=(margin, spacing), pady=(0, margin))
        
        # mention légale
        self.prompt_mention_legale1 = tk.ttk.Label(self.main_frame, text=self.mention_legale_courte1, font=(None, 8))
        self.prompt_mention_legale1.grid(row=6, column=1, columnspan=2, padx=margin, pady=(margin, spacing))
        url_font = tk.font.nametofont("TkDefaultFont").copy()
        url_font.configure(underline=1)
        url_label2 = tk.ttk.Label(
            self.main_frame, text=self.dpo, style="Url.TLabel", cursor="hand2", font=(url_font,8)
        )
        url_label2.grid(row=7, column=1, columnspan=2, padx=margin, pady=(margin, spacing))
        url_label2.bind("<Button-1>", lambda _: webbrowser.open(self.dpo))
        
        # ???
        self.main_frame.columnconfigure(1, weight=1)
        # taper Entrée a la même action que le clic sur "non"
        # self.bind("<Return>", self.on_non, True)
        # print("µµµµµµµµµµµµµµµ" + str(self.main_frame.focus_get()))

        
    def on_oui(self, event=None):
        self.result = "oui"
        self.destroy()

    def on_non(self, event=None):
        self.result = "non"
        self.destroy()
        
    def on_cancel(self, event=None):
        self.result = None
        self.destroy()

    def get_result(self) -> Optional[str]:
        '''
        Renvoie :
        - "oui" si click sur le bouton "oui"
        - "non" si click sur le bouton "non"
        - None si fermeture fenêtre sans click
        '''
        return self.result

    
