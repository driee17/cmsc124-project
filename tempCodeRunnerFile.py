matchfound = re.search("\s", currline)
            if matchfound:
                if matchfound.start() == 0:
                    currline = line[:matchfound.end()]
                    continue