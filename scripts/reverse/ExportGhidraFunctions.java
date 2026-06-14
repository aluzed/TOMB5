// Ghidra Java post-script: export functions, call targets, and callers to CSV.
// Run through analyzeHeadless with:
//   -postScript ExportGhidraFunctions.java /path/to/ghidra-functions.csv

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;

public class ExportGhidraFunctions extends GhidraScript {
    private String csvCell(String value) {
        if (value == null) {
            value = "";
        }
        return "\"" + value.replace("\"", "\"\"") + "\"";
    }

    private String addrToHex(Function function) {
        return String.format("0x%08x", function.getEntryPoint().getOffset());
    }

    private String sortedFunctionNames(java.util.Set<Function> functions) {
        List<Function> list = new ArrayList<Function>(functions);
        Collections.sort(list, new Comparator<Function>() {
            public int compare(Function a, Function b) {
                return Long.compare(a.getEntryPoint().getOffset(), b.getEntryPoint().getOffset());
            }
        });
        List<String> names = new ArrayList<String>();
        for (Function function : list) {
            names.add(function.getName());
        }
        return String.join(";", names);
    }

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 1) {
            throw new IllegalArgumentException("Missing output CSV path argument");
        }

        File out = new File(args[0]);
        File parent = out.getParentFile();
        if (parent != null) {
            parent.mkdirs();
        }

        List<Function> functions = new ArrayList<Function>();
        FunctionIterator iterator = currentProgram.getFunctionManager().getFunctions(true);
        while (iterator.hasNext()) {
            functions.add(iterator.next());
        }
        Collections.sort(functions, new Comparator<Function>() {
            public int compare(Function a, Function b) {
                return Long.compare(a.getEntryPoint().getOffset(), b.getEntryPoint().getOffset());
            }
        });

        PrintWriter writer = new PrintWriter(new FileWriter(out));
        try {
            writer.println("entry,name,body_size,called_functions,callers");
            for (Function function : functions) {
                List<String> row = new ArrayList<String>();
                row.add(String.format("0x%08x", function.getEntryPoint().getOffset()));
                row.add(function.getName());
                row.add(Long.toString(function.getBody().getNumAddresses()));
                row.add(sortedFunctionNames(function.getCalledFunctions(monitor)));
                row.add(sortedFunctionNames(function.getCallingFunctions(monitor)));

                List<String> escaped = new ArrayList<String>();
                for (String cell : row) {
                    escaped.add(csvCell(cell));
                }
                writer.println(String.join(",", escaped));
            }
        }
        finally {
            writer.close();
        }

        println("Exported " + functions.size() + " functions to " + out.getAbsolutePath());
    }
}
