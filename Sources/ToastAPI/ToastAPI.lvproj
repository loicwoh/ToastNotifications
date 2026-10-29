<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="26008000">
	<Property Name="NI.LV.All.SaveVersion" Type="Str">26.0</Property>
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Property Name="NI.Project.Description" Type="Str">ToastAPI: pure LabVIEW content and notification contracts. The Windows backend is not implemented yet.</Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Examples" Type="Folder">
			<Item Name="Build Reply Content.vi" Type="VI" URL="../Examples/Build Reply Content.vi"/>
		</Item>
		<Item Name="Typedefs" Type="Folder">
			<Item Name="Activation.ctl" Type="VI" URL="../Types/Activation.ctl"/>
			<Item Name="Argument.ctl" Type="VI" URL="../Types/Argument.ctl"/>
			<Item Name="Button.ctl" Type="VI" URL="../Types/Button.ctl"/>
			<Item Name="Content Data.ctl" Type="VI" URL="../Types/Content Data.ctl"/>
			<Item Name="Text Input.ctl" Type="VI" URL="../Types/Text Input.ctl"/>
		</Item>
		<Item Name="ActivationHandler.lvclass" Type="LVClass" URL="../Classes/ActivationHandler/ActivationHandler.lvclass"/>
		<Item Name="ToastContent.lvclass" Type="LVClass" URL="../Classes/ToastContent/ToastContent.lvclass"/>
		<Item Name="ToastService.lvclass" Type="LVClass" URL="../Classes/ToastService/ToastService.lvclass"/>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
