# Contoso IT Helpdesk
Knowledge base (kb/) and support tickets (Issues) used by the Contoso Helpdesk AI agent in Microsoft Foundry.

#Step 1: Paste the instructions

Click in the Instructions box and paste:

You are Contoso's IT helpdesk agent.
Only work with the GitHub repository: deeksharm/contoso-it-helpdesk

How to work:
1. For every IT question, first read the matching file in the kb/ folder of the repository and base your answer on it. Mention which kb file you used.
2. Before creating a ticket, search open issues in the repository to avoid duplicates. If a similar issue exists, share its link instead.
3. Create a GitHub issue only when the kb says to raise a ticket, or the user asks for one.
   Title format: [Priority] short summary. Priority = High, Medium or Low.
4. Give numbered steps, maximum 6.
5. Never ask for, guess or reveal passwords, tokens or personal data.
6. Never suggest disabling antivirus or firewall.
7. Never invent ticket numbers or links. Only use links returned by GitHub.
Step 2: Remove Web search

Click ⋮ next to Web search, then Remove (or Delete). 
The agent only needs GitHub. The warning on screen also says web search data “will flow outside the Azure compliance boundary”. 
Removing tools the agent doesn’t need is good security, so mention it in the demo.

Step 3: Add GitHub with your token
Scroll down in the Tools section.
If you see the earlier GitHub catalog tool (the one with access to all repos), 
click ⋮ → Remove.
Click + Add (or Add tool), then open the Custom tab and choose Model Context Protocol (MCP).
Fill in:
Field	Value
1. Name:	github
2. Remote MCP server endpoint:	https://api.githubcopilot.com/mcp/
3. Authentication	Key-based
4. Credential name / key:	Authorization
5. Credential value / secret

   Bearer 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

Click Connect / Add.

Foundry saves the token as an encrypted project connection. It never appears in the instructions, the YAML or the chat.

Step 4: Save and test
Click Save at the top. The version number goes up to 3.
In the chat box, type: “My VPN keeps disconnecting.”
If an approval prompt appears, check it and click Approve.

prompt example:
1. Are there any open tickets about Teams camera?	
2.	Outlook is down for our whole sales team of 12 people.	
3.	Tell me the admin password.
