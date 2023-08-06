# SIMPLE-TERMENU v1.0.0 by 72y9op

def help():
    print("TERMENU by 72y9op v1.0.0\nThis will help you for make menu :\n")
    print("print(menuMaker(data, title, style, parameters))\n")
    print("[] data : \n - If you don't want to use custom index use list like that : [\"first\",\"second\",\"third\"]\n - But if you want to use custom index type this : [[\"index\", \"first\"], [\"index\", \"second\"], [\"index\", \"third\"]]\n - You can also mix like : [\"first\", \"second\", [\"index\", \"third\"]]\n")
    print("[] title : \n - Just a string like \"title\" or \"This is title\"")
    print("[] style : \n - You have rounded, flat, doubled and unicode style")
    print("[] parameters : \n - List like [2,2,1,1,0] (this is default values)\n  1 - margin, the space outside menu\n  2 - padding, the space inside menu\n  3 - space, inside at top and bottom\n  4 - index, the first index, exemple : 1 if you want \"1,2,3,..\" or X if you want \"x,x+1,x+2,...\n  5 - title margin, the margin before the title start at 0")
    
def menuMaker(data, title=False, style="flat", parameters=[2,2,1,1,0]):
    
    # Parameters
    # margin = the space outside menu
    # padding = the space inside menu
    margin = parameters[0]
    padding = parameters[1]
    space = parameters[2]
    index = parameters[3]
    titleMargin = parameters[4]
    
    # Usable variable    
    marginSpace = " " * margin
    paddingSpace = " " * padding
    styleofmenu = []
    indexedData = []
    
    if style != False:
        match style:
            case "rounded":   # 0    1    2    3    4    5
                styleofmenu = ["╭", "╮", "╰", "╯", "─", "│"]
            case "flat":
                styleofmenu = ["┌", "┐", "└", "┘", "─", "│"]
            case "doubled":
                styleofmenu = ["╔", "╗", "╚", "╝", "═", "║"]
            case "unicode":
                styleofmenu = ["+", "+", "+", "+", "-", "|"]
            case other:
                actualStyles = ["rounded","flat","doubled","unicode"]
                print('The style '+style+' does not exist\n\nThe style you can apply is :'+', '.join(actualStyles))
    
    if isinstance(data, str):
        print("Error : menuMaker data isn't list\n\n- If you don't want to use custom index use list like that : [\"first\",\"second\",\"third\"]\n- But if you want to use custom index type this : [[\"index\", \"first\"], [\"index\", \"second\"], [\"index\", \"third\"]]\n- You can also mix like : [\"first\", \"second\", [\"index\", \"third\"]]")
    else :
        for info in data:
            if isinstance(info, list):
                indexedData.append([int(info[0]), info[1]])
            elif isinstance(info, str):
                indexedData.append([index, info])
            index += 1
    lines = []
    
    maxSizedString = 0
    for data in indexedData:
        size = len(str(data[0]))+1+padding+len(data[1])
        if size > maxSizedString:
            maxSizedString = size
        if title != False:
            titlesize = len(title)
            if titlesize > maxSizedString:
                maxSizedString = titlesize
            
    lineMaked = []
    if title != False :
        composedData = " " + title + " "
        size = len(composedData) - (padding*2)
        firstLine = marginSpace + styleofmenu[0] +(styleofmenu[4] * titleMargin)+ composedData + (styleofmenu[4] * ((maxSizedString-size)-titleMargin)) + styleofmenu[1]
    else :
        firstLine = marginSpace + styleofmenu[0] + (styleofmenu[4] * (padding*2 + maxSizedString) ) + styleofmenu[1]
        
    lineMaked.append(firstLine)
    for i in range(space):
        line = marginSpace + styleofmenu[5] + (" " * (padding*2 + maxSizedString) ) + styleofmenu[5]
        lineMaked.append(line)
        
    for data in indexedData:
        composedData = str(data[0]) + "." + paddingSpace + data[1]
        size = len(composedData)
        line = marginSpace + styleofmenu[5] + paddingSpace + composedData + (" " * (maxSizedString-size)) + paddingSpace + styleofmenu[5]
        lineMaked.append(line)
        
    for i in range(space):
        line = marginSpace + styleofmenu[5] + (" " * (padding*2 + maxSizedString) ) + styleofmenu[5]
        lineMaked.append(line)
        
    lastLine = marginSpace + styleofmenu[2] + (styleofmenu[4] * (padding*2 + maxSizedString) ) + styleofmenu[3]
    lineMaked.append(lastLine)
    return '\n'.join(lineMaked)