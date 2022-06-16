import React, { useState } from "react";
import { Table, TableBody, TableCell, TableHead, TableRow, Dialog, DialogActions, DialogTitle, DialogContent, Button } from "@mui/material";
import RestartAltIcon from "@mui/icons-material/RestartAlt";

import Title from "./title";
import { TASK } from "../constant";

export default (props) => {
    const sendData = props["sendData"];
    const list = [{ icon: <RestartAltIcon />, operation: "Reset", discription: "Reset the bed to sleepable position" }];
    const reset = () => {
        sendData(TASK.RESET);
    };

    return (
        <React.Fragment>
            <Title>Settings</Title>
            <Table size="medium">
                <TableHead>
                    <TableCell>Operation</TableCell>
                    <TableCell>Discription</TableCell>
                </TableHead>
                <TableBody>
                    {list.map((item) => (
                        <TableRow>
                            <TableCell>
                                <Button variant="outlined" startIcon={item["icon"]} onClick={reset}>
                                    {item["operation"]}
                                </Button>
                            </TableCell>
                            <TableCell>{item["discription"]}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </React.Fragment>
    );
};
