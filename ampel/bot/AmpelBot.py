
from ampel.abstract.AbsProcessorUnit import AbsProcessorUnit
from ampel.cli.ArgParserBuilder import ArgParserBuilder
from ampel.cli.BufferCommand import BufferCommand
from ampel.cli.T2Command import T2Command

from typing import Any, Dict, List
  
from slack import WebClient
from slack.errors import SlackClientError
from slack.web.slack_response import SlackResponse
from slackeventsapi import SlackEventAdapter
#from flask import Flask
#import logging
import subprocess
  
from slack import RTMClient, AsyncWebClient


class AmpelBot(AbsProcessorUnit):

    slack_token: str = "xoxb-xxxxxxxxxxxxx-xxxxxxxxxxxxx-xxxxxxxxxxxxx"
    slack_channel: str = "general"
    ampel_conf: str = "ampel_conf.yaml"
    save_file: str = "file.html"  # the file in which the output of ampel command is saved   
#    user: str = 
    valid_ops : Dict[str, List[str]] = {
                        'log' : ['show', 'save', 'help'] ,
                        't2': ['show', 'save', 'help']
                         }

    def __init__(self):
        self.rtm_client = RTMClient(token=self.slack_token)
        self.rtm_client.run_on(event='message')(self.message)


    def run(self) -> Any:
#        os.environ['AMPELCONF'] = self.ampel_conf
        self.rtm_client.start()

#    async def on_message(self, **payload) -> None:
#    @RTMClient.run_on(event="message")
    def message(self, **payload):
        def upload_file(file):
            with open(self.save_file, 'rb') as att:
                 wc.files_upload(
                     file = att,
                     channels=self.slack_channel,
                     thread_ts= thread_ts,
                     filename= 'save_file',
                     title= f'Attachment\'s file {self.save_file}:',
                     initial_comment = "You requested ampel log. \n"
                                      f"The output is saved at: ```{self.save_file}```",
                     )
                
  
        data = payload["data"]
        wc = payload["web_client"]
  
        if "text" in data.keys():            
            slacktext = data["text"]
            slacktext = slacktext.replace("*", "")
            opt = slacktext.split(" ")
  
            if opt[0] and opt[0].lower() in ["ampel"]:
                thread_ts = data["ts"]

                if len(opt) == 1 :
                    p = subprocess.Popen(opt[0].lower(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                    out, err = p.communicate() 
                    outformat = out.decode('utf8').strip()
  
                    blocks = [
                              {
                                  "type": "section",
                                  "text": {
                                      "type": "mrkdwn",
                                      "text": f"You requested {opt}. The output is:\n"
                                              f"```{outformat}```",
                                          },
                              }
                    ]

                elif len(opt) >= 2:
                    import re
                    if not re.search('-config', slacktext):
                        slacktext=slacktext+" -config "+self.ampel_conf
                   
                    if opt[1] not in self.valid_ops:
                        blocks = [
                                 {
                                  "type": "section",
                                  "text": {
                                      "type": "mrkdwn",
                                      "text": "You requested an invalid option.",
                                          },
                              }
                         ]

                    elif opt[1] in self.valid_ops.keys(): 
                        if opt[2] == "show":
                            logfile = open(self.save_file, 'w+')
                            p = subprocess.Popen(slacktext, stdout=logfile, shell=True)
                            p.wait()
                            upload_file(self.save_file)
  
                        elif opt[2] == "save":
                               try:
                                   self.save_file=re.search(r'(?<=-out )[^\s]*', slacktext).group()
                                   pass
                               except:
                                   blocks = [
                                            {
                                             "type": "section",
                                             "text": { 
                                                 "type": "mrkdwn",
                                                 "text": "Wrong command syntax. Check if you have included -out.",
                                                     },
                                            }
                                   ]     
                               else:    
                                   p = subprocess.Popen(slacktext, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True )
                                   p.wait()
                                   upload_file(self.save_file)


            wc.chat_postMessage(
                channel=self.slack_channel,
                blocks=blocks,
                thread_ts=thread_ts,
                icon_emoji=":fp-emoji:",
            )



if __name__ == "__main__":
    AmpelBot().run()
